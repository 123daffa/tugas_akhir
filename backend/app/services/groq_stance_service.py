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
# Selain "Fakta", urutan mengikuti spektrum low->high harm dari "7 Types of
# Mis- and Disinformation" (First Draft, Claire Wardle 2019) -- kalau seri,
# kategori dengan tuduhan paling ringan yang menang lebih dulu (pendekatan
# konservatif, tidak langsung lompat ke tuduhan terberat).
URUTAN_TIE_BREAK = [
    "Satire atau Parodi",
    "False Connection",
    "Misleading Content",
    "False Context",
    "Imposter Content",
    "Manipulated Content",
    "Fabricated Content",
    "Fakta",
]

# Kategori default kalau parsing/klasifikasi Groq gagal atau hasilnya di luar
# KATEGORI_VALID. Dipilih "Fabricated Content" karena ini kategori paling
# "aman secara default" -- gagal analisis dianggap sebagai kasus paling
# berisiko tinggi (bukan otomatis dianggap Fakta atau tuduhan ringan).
KATEGORI_FALLBACK = "Fabricated Content"

# 8 kategori final, dipakai untuk inisialisasi breakdown vote supaya semua
# key selalu ada di hasil akhir (meskipun jumlahnya 0).
SEMUA_KATEGORI = [
    "Fakta",
    "Satire atau Parodi",
    "False Connection",
    "Misleading Content",
    "False Context",
    "Imposter Content",
    "Manipulated Content",
    "Fabricated Content",
]


def vote_single_article_klasifikasi(claim: str, article: dict) -> dict:
    """Bandingkan klaim vs isi SATU artikel (snippet Tavily, field 'content'),
    Groq langsung memutuskan salah satu dari 8 kategori final -- dinilai
    SATU artikel per panggilan, bukan gabungan sekaligus."""
    title = article.get("title", "Tanpa judul")
    snippet = article.get("content", "")  # potongan isi artikel (snippet) maksimal 3000 karakter
    prompt = build_prompt_klasifikasi(claim, title, snippet)

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_completion_tokens=512,   # naik dari 200 -> ada ruang untuk reasoning + JSON output
            reasoning_effort="low",
            response_format={"type": "json_object"}
        )
        hasil = json.loads(response.choices[0].message.content)
        if hasil.get("klasifikasi") not in KATEGORI_VALID:
            hasil["klasifikasi"] = KATEGORI_FALLBACK
        return hasil
    except Exception as e:
        print(f"[WARNING] Gagal klasifikasi 1 artikel: {e}")
        return {"klasifikasi": KATEGORI_FALLBACK, "alasan": "Gagal dianalisis"}


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
    Klasifikasi ke 8 kategori (Fakta / Satire atau Parodi / False Connection /
    Misleading Content / False Context / Imposter Content / Manipulated
    Content / Fabricated Content) berdasarkan MAJORITY VOTE MURNI (plurality,
    hitungan biasa per artikel) dari hasil klasifikasi Groq. Bobot skor
    kredibilitas Tavily TIDAK DIPAKAI di sini. Kalau seri, tie-break pakai
    URUTAN_TIE_BREAK.
    """
    if not selected_articles:
        return {
            "klasifikasi": KATEGORI_FALLBACK,
            "confidence_score": 0.0,
            "stance_breakdown": {kategori: 0 for kategori in SEMUA_KATEGORI},
            "alasan_per_artikel": []
        }

    breakdown = {kategori: 0 for kategori in SEMUA_KATEGORI}
    alasan_list = []

    print(f"[INFO] Mulai klasifikasi majority vote untuk {len(selected_articles)} artikel...")

    for i, article in enumerate(selected_articles, start=1):
        print(f"[INFO] ({i}/{len(selected_articles)}) Klasifikasi: {article.get('title', 'Tanpa judul')}")
        hasil = vote_single_article_klasifikasi(claim, article)
        klasifikasi = hasil.get("klasifikasi", KATEGORI_FALLBACK)
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