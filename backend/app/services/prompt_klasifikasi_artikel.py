KATEGORI_VALID = {"Fakta", "False Content", "Misleading Content", "Fabricated Content"}


def build_prompt_klasifikasi(claim: str, title: str, snippet: str) -> str:
    """
    Template prompt TUNGGAL untuk klasifikasi artikel vs klaim -- dipakai
    SAMA PERSIS oleh groq_stance_service.py (teks-saja) dan
    groq_stance_gambar_service.py (gambar/video), supaya perbaikan prompt
    (hasil 4 iterasi debugging) tidak perlu disalin manual ke dua tempat.
    Yang boleh beda antar pemanggil HANYA panjang potongan snippet-nya.
    """
    return f"""Kamu adalah asisten fact-checking. Bandingkan klaim berikut
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
- False Content: klaim sepenuhnya dikarang / tidak berdasar dari kejadian nyata manapun
- Misleading Content: sebagian klaim benar, tapi kesimpulan/konteksnya menyesatkan
- Fabricated Content: klaim bertentangan dengan isi artikel, atau inti klaim sama sekali tidak dibahas klaim sepenuhnya dikarang / tidak berdasar dari kejadian nyata manapun

Jawab HANYA JSON: {{"klasifikasi": "Fakta"/"False Content"/"Misleading Content"/"Fabricated Content", "alasan": "..."}}"""