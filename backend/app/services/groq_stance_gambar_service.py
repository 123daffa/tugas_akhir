import json
from groq import Groq
from app.core.config import settings
from app.core.constants import GROQ_MODEL_NAME

groq_client = Groq(api_key=settings.GROQ_API_KEY)

KATEGORI_VALID = {"Fakta", "False Content", "Misleading Content", "Fabricated Content"}

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
    snippet = article.get("content", "")[:1000]

    prompt = f"""Kamu adalah asisten fact-checking. Bandingkan klaim berikut
dengan isi artikel berita, lalu klasifikasikan ke SALAH SATU dari 4 kategori.

KLAIM: {claim}

ARTIKEL:
Judul: {title}
Cuplikan: {snippet}

PENTING -- perhatikan pola ini sebelum memutuskan, ikuti urutan prioritas berikut:

PRIORITAS 1 -- Cek dulu apakah klaim berbentuk SEBAB-AKIBAT (mengandung kata
"karena", "sehingga", "akibatnya", "makanya", dsb, yang menghubungkan sebuah
ALASAN dengan sebuah KESIMPULAN/TINDAKAN). Kalau ya, kamu WAJIB menilai
KESIMPULAN/TINDAKAN-nya secara terpisah dari alasannya -- JANGAN menyimpulkan
klaim "Fakta" hanya karena bagian ALASANNYA benar. Contoh: klaim "X bebas
hukuman KARENA barang bukti palsu" punya dua bagian: (a) barang bukti palsu,
dan (b) X bebas hukuman. Kalau artikel cuma mengonfirmasi (a) tapi TIDAK
mengonfirmasi/malah membantah (b), klaim keseluruhan TIDAK BOLEH "Fakta" --
paling tepat "Misleading Content" (sebagian benar, tapi kesimpulannya salah/
menyesatkan) atau "False Content" (kalau kesimpulannya jelas dibantah).

PRIORITAS 2 -- Kalau judul artikel mengandung tag DEBUNKING EKSPLISIT seperti
"[SALAH]", "[HOAKS]", "Cek Fakta:", "Keliru:", "Klarifikasi:", "Hoaks,"/"Hoaks:",
itu adalah VONIS bahwa SELURUH NARASI dalam klaim (termasuk kesimpulan sebab-
akibatnya, bukan cuma detail kecil di dalamnya) tidak benar/menyesatkan. Tag
ini MENGALAHKAN kecocokan substansi parsial -- jangan biarkan kecocokan
sebagian fakta (Prioritas 3) membuatmu mengabaikan vonis tag ini.

PRIORITAS 3 -- Kalau tidak ada tag debunking dan klaim bukan sebab-akibat:
"Fakta" tidak mengharuskan kata-kata persis sama, cukup substansi/inti klaim
didukung isi artikel. "False Content" kalau bertentangan atau inti klaim sama
sekali tidak dibahas.

PRIORITAS 4 -- Sebelum menjawab, pastikan ALASAN yang kamu tulis konsisten
dengan kategori yang dipilih dan merujuk ke ISI artikel (bukan cuma judul).

Pilih SATU kategori:
- Fakta: substansi/inti klaim (termasuk kesimpulan sebab-akibatnya kalau ada) didukung oleh isi artikel
- False Content: klaim bertentangan dengan isi artikel, atau inti klaim sama sekali tidak dibahas
- Misleading Content: sebagian klaim benar, tapi kesimpulan/konteksnya menyesatkan
- Fabricated Content: klaim sepenuhnya dikarang / tidak berdasar dari kejadian nyata manapun

Jawab HANYA JSON: {{"klasifikasi": "Fakta"/"False Content"/"Misleading Content"/"Fabricated Content", "alasan": "..."}}"""

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