import json
from groq import Groq
from app.core.config import settings
from app.core.constants import GROQ_MODEL_NAME
from app.services.prompt_klasifikasi_artikel import build_prompt_klasifikasi
from app.core.constants import KATEGORI_VALID

groq_client = Groq(api_key=settings.GROQ_API_KEY)

# Urutan prioritas tie-break kalau ada 2+ kategori dengan jumlah suara sama-sama
# tertinggi. "Fakta" sengaja diletakkan PALING TERAKHIR -- kesimpulan positif
# hanya boleh menang lewat mayoritas jelas, bukan kebetulan hasil seri.
# "Misleading Content" diletakkan PALING ATAS karena maknanya paling
# merepresentasikan situasi ambigu (sebagian sumber bilang benar, sebagian salah).
URUTAN_TIE_BREAK = ["Misleading Content", "False Content", "Fabricated Content", "Fakta"]


def vote_single_article_klasifikasi(claim: str, article: dict) -> dict:
    """Bandingkan klaim vs isi SATU artikel (snippet Tavily, field 'content'),
    Groq langsung memutuskan salah satu dari 4 kategori final -- dinilai
    SATU artikel per panggilan, bukan gabungan sekaligus."""
    title = article.get("title", "Tanpa judul")
    snippet = article.get("content", "")[:500]
    prompt = build_prompt_klasifikasi(claim, title, snippet)

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=200,
            response_format={"type": "json_object"}
        )
        hasil = json.loads(response.choices[0].message.content)
        if hasil.get("klasifikasi") not in KATEGORI_VALID:
            hasil["klasifikasi"] = "False Content"
        return hasil
    except Exception as e:
        print(f"[WARNING] Gagal klasifikasi 1 artikel: {e}")
        return {"klasifikasi": "False Content", "alasan": "Gagal dianalisis"}

def _tentukan_pemenang_vote(breakdown: dict) -> str:
    """
    Vote terbanyak (plurality) menentukan pemenang. Kalau ada 2+ kategori
    dengan jumlah suara sama-sama tertinggi (seri), tie-break berdasarkan
    URUTAN_TIE_BREAK -- kategori paling "hati-hati" menang, "Fakta" tidak
    pernah menang lewat seri.
    """
    skor_tertinggi = max(breakdown.values())
    kandidat_seri = [kategori for kategori, jumlah in breakdown.items() if jumlah == skor_tertinggi]

    if len(kandidat_seri) == 1:
        return kandidat_seri[0]

    for kategori in URUTAN_TIE_BREAK:
        if kategori in kandidat_seri:
            return kategori

    return kandidat_seri[0]  # fallback, seharusnya tidak pernah tercapai


def classify_text_by_stance(claim: str, selected_articles: list) -> dict:
    """
    Klasifikasi ke 4 kategori (Fakta / False Content / Misleading Content /
    Fabricated Content) berdasarkan MAJORITY VOTE MURNI (plurality, hitungan
    biasa per artikel) dari hasil klasifikasi Groq. Bobot skor kredibilitas
    Tavily TIDAK DIPAKAI di sini. Kalau seri, tie-break pakai URUTAN_TIE_BREAK.
    """
    if not selected_articles:
        return {
            "klasifikasi": "False Content",
            "confidence_score": 0.0,
            "stance_breakdown": {"Fakta": 0, "False Content": 0, "Misleading Content": 0, "Fabricated Content": 0},
            "alasan_per_artikel": []
        }

    breakdown = {"Fakta": 0, "False Content": 0, "Misleading Content": 0, "Fabricated Content": 0}
    alasan_list = []

    print(f"[INFO] Mulai klasifikasi majority vote untuk {len(selected_articles)} artikel...")

    for i, article in enumerate(selected_articles, start=1):
        print(f"[INFO] ({i}/{len(selected_articles)}) Klasifikasi: {article.get('title', 'Tanpa judul')}")
        hasil = vote_single_article_klasifikasi(claim, article)
        klasifikasi = hasil.get("klasifikasi", "False Content")
        breakdown[klasifikasi] += 1

        alasan_list.append({
            "judul": article.get("title", "Tanpa judul"),
            "url": article.get("url", "#"),
            "stance": klasifikasi,
            "alasan": hasil.get("alasan", "")
        })

    print("[INFO] Selesai klasifikasi majority vote.")

    total_artikel = len(selected_articles)
    klasifikasi_final = _tentukan_pemenang_vote(breakdown)
    confidence = round(breakdown[klasifikasi_final] / total_artikel, 4)

    return {
        "klasifikasi": klasifikasi_final,
        "confidence_score": confidence,
        "stance_breakdown": breakdown,
        "alasan_per_artikel": alasan_list
    }