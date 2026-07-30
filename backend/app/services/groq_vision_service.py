import json
import requests
import base64
from io import BytesIO
from PIL import Image
from groq import Groq
from app.core.config import settings
from app.core.constants import GROQ_VISION_MODEL_NAME
from app.core.constants import IMAGE_RELEVANCE_THRESHOLD

groq_client = Groq(api_key=settings.GROQ_API_KEY)

MAX_DIMENSION = 512  # resize gambar biar hemat token, cukup untuk vision task ini
JPEG_QUALITY = 70


def _compress_image_bytes(image_bytes: bytes) -> bytes:
    """
    Resize + kompres gambar sebelum dikirim ke Groq Vision, supaya ukuran
    base64 (dan token yang dihitung) jauh lebih kecil. Vision model tidak
    butuh resolusi tinggi untuk membandingkan kemiripan gambar.
    """
    try:
        img = Image.open(BytesIO(image_bytes))
        img = img.convert("RGB")  # buang alpha channel, standarkan ke JPEG
        img.thumbnail((MAX_DIMENSION, MAX_DIMENSION))

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=JPEG_QUALITY)
        return buffer.getvalue()
    except Exception as e:
        print(f"[WARNING] Gagal kompres gambar, pakai versi asli: {e}")
        return image_bytes


def _bytes_to_data_uri(image_bytes: bytes, compress: bool = True) -> str:
    """Ubah bytes gambar jadi base64 data URI, dengan opsi kompresi dulu."""
    if compress:
        image_bytes = _compress_image_bytes(image_bytes)
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"


def compress_image_to_data_uri(image_bytes: bytes) -> str:
    """
    Versi publik dari _bytes_to_data_uri, untuk dipakai di luar modul ini
    (misal di route Flask saat memproses gambar upload user).
    """
    return _bytes_to_data_uri(image_bytes, compress=True)


def _fetch_image_as_data_uri(image_url: str, timeout: int = 5) -> str | None:
    """
    Unduh gambar dari URL eksternal (misal dari artikel Tavily), kompres,
    lalu ubah jadi base64 data URI. Diperlukan karena beberapa website
    memblokir hotlinking/bot request langsung dari server Groq (403),
    dan supaya ukurannya tidak membengkakkan jumlah token request.
    Kalau gagal (403, timeout, bukan gambar, dsb), return None -- artikel
    itu nanti dilewati, bukan bikin seluruh request gagal.
    """
    # Skip format non-raster (SVG, dll) sebelum sempat request -- Pillow
    # tidak bisa memprosesnya, dan biasanya ini logo/header situs,
    # bukan gambar konten artikel yang relevan untuk dibandingkan.
    if image_url.lower().split("?")[0].endswith(".svg"):
        return None

    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; FactCheckBot/1.0)"}
        resp = requests.get(image_url, headers=headers, timeout=timeout)
        resp.raise_for_status()

        content_type = resp.headers.get("Content-Type", "image/jpeg").split(";")[0]
        if not content_type.startswith("image/") or content_type == "image/svg+xml":
            return None

        return _bytes_to_data_uri(resp.content, compress=True)
    except Exception as e:
        print(f"[WARNING] Gagal unduh gambar referensi {image_url}: {e}")
        return None


def verify_image_relevance(user_image_url: str, caption: str, tavily_images: list) -> dict:
    """
    Bandingkan gambar user dengan gambar-gambar dari SATU artikel,
    dan cek kesesuaian gambar dengan caption user.
    Groq Vision yang menilai langsung (bukan similarity manual/CLIP).

    tavily_images: list URL gambar milik satu artikel.
    Model qwen/qwen3.6-27b maksimal terima 3 gambar per request,
    jadi dipotong maks 2 gambar referensi + 1 gambar user = 3 total.
    Tiap gambar referensi diunduh & dikompres dulu jadi base64, biar tidak
    kena blokir hotlinking (403) dan tidak melebihi limit token per menit.
    """
    kandidat_referensi = tavily_images[:2]

    reference_data_uris = []
    for img_url in kandidat_referensi:
        data_uri = _fetch_image_as_data_uri(img_url)
        if data_uri:
            reference_data_uris.append(data_uri)

    if not reference_data_uris:
        return {
            "relevance_score": 0,
            "penjelasan": "Tidak ditemukan gambar pembanding dari hasil pencarian berita (gagal diunduh atau tidak tersedia)."
        }

    content = [
        {"type": "text", "text": f"""Kamu adalah asisten fact-checking gambar.

CAPTION YANG DIKLAIM USER: "{caption}"

Gambar PERTAMA di bawah adalah gambar yang diunggah user.
Gambar-gambar SETELAHNYA adalah gambar yang ditemukan dari artikel berita terkait topik ini.

Tugasmu:
1. Apakah gambar user MIRIP/SAMA dengan salah satu gambar referensi (indikasi gambar ini
   memang berasal dari kejadian/konteks yang diberitakan)?
2. Apakah isi gambar user SESUAI dengan caption yang diklaim?

Berikan skor RELEVANSI dari 0-100 (semakin tinggi = semakin yakin gambar ini
memang asli dari konteks yang diklaim, bukan gambar lama/tidak berhubungan/di luar konteks).

WAJIB jawab HANYA JSON: {{"relevance_score": <0-100>, "penjelasan": "<2-3 kalimat>"}}"""},
        {"type": "image_url", "image_url": {"url": user_image_url}},
    ]

    for data_uri in reference_data_uris:
        content.append({"type": "image_url", "image_url": {"url": data_uri}})

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_VISION_MODEL_NAME,
            messages=[{"role": "user", "content": content}],
            temperature=0.7,
            max_tokens=300,
            reasoning_effort="none",
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"[ERROR] Groq Vision relevansi gambar gagal: {e}")
        return {
            "relevance_score": 0,
            "penjelasan": "Gagal menganalisis gambar, dianggap tidak dapat diverifikasi."
        }


def verify_image_relevance_per_artikel(image_url: str, caption: str, selected_articles: list, max_artikel: int = 2) -> dict:
    """
    Verifikasi relevansi gambar user terhadap gambar milik masing-masing artikel
    (bukan pool gabungan). Loop tiap artikel -> nilai satu-satu -> agregasi
    dengan bobot skor Tavily, sama seperti pola voting stance teks
    (vote_single_article_stance -> classify_text_by_stance).

    Untuk menjaga latensi tetap wajar, hanya `max_artikel` artikel dengan
    skor Tavily TERTINGGI yang dicek gambarnya (bukan semua selected_articles).
    Artikel tanpa gambar tetap dilewati (tidak ikut menyumbang bobot).
    """
    # Urutkan dulu berdasarkan skor Tavily, ambil yang paling relevan saja
    artikel_untuk_dicek = sorted(
        selected_articles, key=lambda a: a.get("score", 0), reverse=True
    )[:max_artikel]

    weighted_score = 0.0
    total_weight = 0.0
    detail_per_artikel = []

    print(f"[INFO] Mulai cek relevansi gambar untuk {len(artikel_untuk_dicek)} artikel (dari {len(selected_articles)} artikel terpilih)...")

    for i, article in enumerate(artikel_untuk_dicek, start=1):
        gambar_artikel = article.get("images", [])
        if not gambar_artikel:
            continue

        print(f"[INFO] ({i}/{len(artikel_untuk_dicek)}) Cek gambar artikel: {article.get('title', 'Tanpa judul')}")
        hasil = verify_image_relevance(image_url, caption, gambar_artikel)
        skor = hasil.get("relevance_score", 0)
        weight = article.get("score", 0.5)

        weighted_score += skor * weight
        total_weight += weight

        detail_per_artikel.append({
            "judul": article.get("title", "Tanpa judul"),
            "url": article.get("url", "#"),
            "relevance_score": skor,
            "penjelasan": hasil.get("penjelasan", "")
        })

    print("[INFO] Selesai cek relevansi gambar untuk semua artikel.")

    if total_weight == 0:
        return {
            "relevance_score": 0,
            "penjelasan": "Tidak ada artikel dengan gambar untuk dibandingkan.",
            "artikel_paling_relevan": None,
            "detail_per_artikel": []
        }

    skor_akhir = round(weighted_score / total_weight, 2)
    artikel_paling_relevan = max(detail_per_artikel, key=lambda x: x["relevance_score"])

    return {
        "relevance_score": skor_akhir,
        "penjelasan": artikel_paling_relevan["penjelasan"],
        "artikel_paling_relevan": artikel_paling_relevan["judul"],
        "detail_per_artikel": detail_per_artikel
    }