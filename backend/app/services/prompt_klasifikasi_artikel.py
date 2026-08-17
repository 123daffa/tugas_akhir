KATEGORI_VALID = {
    "Fakta",
    "Satire atau Parodi",
    "False Connection",
    "Misleading Content",
    "False Context",
    "Imposter Content",
    "Manipulated Content",
    "Fabricated Content",
}

def build_prompt_klasifikasi(claim: str, title: str, snippet: str) -> str:
    """
    Template prompt TUNGGAL untuk klasifikasi artikel vs klaim -- dipakai
    SAMA PERSIS oleh groq_stance_service.py (teks-saja) dan
    groq_stance_gambar_service.py (gambar/video), supaya perbaikan prompt
    (hasil 4 iterasi debugging) tidak perlu disalin manual ke dua tempat.
    Yang boleh beda antar pemanggil HANYA panjang potongan snippet-nya.
    """
    return f"""Kamu adalah asisten fact-checking. Bandingkan klaim berikut
dengan isi artikel berita, lalu klasifikasikan ke SALAH SATU dari 8 kategori
di bawah ini.

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
pilih kategori yang paling sesuai dengan cara kesimpulannya salah/menyesatkan
(lihat definisi kategori di bawah).

PRIORITAS 2 -- Kalau judul artikel mengandung tag DEBUNKING EKSPLISIT seperti
"[SALAH]", "[HOAKS]", "Cek Fakta:", "Keliru:", "Klarifikasi:", "Hoaks,"/"Hoaks:",
itu adalah VONIS bahwa SELURUH NARASI dalam klaim (termasuk kesimpulan sebab-
akibatnya, bukan cuma detail kecil di dalamnya) tidak benar/menyesatkan. Tag
ini MENGALAHKAN kecocokan substansi parsial -- jangan biarkan kecocokan
sebagian fakta (Prioritas 3) membuatmu mengabaikan vonis tag ini.

PRIORITAS 3 -- Kalau tidak ada tag debunking dan klaim bukan sebab-akibat:
"Fakta" tidak mengharuskan kata-kata persis sama, cukup substansi/inti klaim
-- termasuk detail spesifik seperti jenis objek, jumlah, lokasi, dan waktu
kejadian -- didukung isi artikel. Kalau ada detail spesifik yang berbeda atau
tidak dibahas artikel, atau klaim bertentangan/tidak dibahas sama sekali,
klaim BUKAN "Fakta" -- pilih salah satu dari 7 kategori disinformasi di bawah
sesuai CARA klaim itu menyimpang dari artikel.

PRIORITAS 4 -- Sebelum menjawab, pastikan ALASAN yang kamu tulis konsisten
dengan kategori yang dipilih dan merujuk ke ISI artikel (bukan cuma judul).
Kalau alasanmu menyebut klaim "tidak didukung", "tidak disebutkan", atau
"berbeda dari artikel", klasifikasi TIDAK BOLEH "Fakta".

PRIORITAS 4 -- Sebelum menjawab, pastikan ALASAN yang kamu tulis konsisten
dengan kategori yang dipilih, menyebut secara eksplisit CIRI dari kategori
tersebut (mis. "konteksnya diputarbalikkan", "sumbernya dipalsukan",
"videonya sudah diedit"), dan merujuk ke ISI artikel (bukan cuma judul).

Pilih SATU kategori (diurutkan dari dampak paling rendah ke paling tinggi,
mengacu pada "7 Types of Mis- and Disinformation" - First Draft, Claire
Wardle 2019). CATATAN soal level HARM di bawah: ini mengukur seberapa besar
POTENSI KERUGIAN/BAHAYA yang ditimbulkan konten tersebut ke pembaca atau
masyarakat kalau dipercaya -- dilihat dari dua hal: (1) seberapa BESAR NIAT
MENIPU di baliknya (tidak sengaja vs sengaja direkayasa penuh), dan (2)
seberapa SULIT dikenali sebagai palsu oleh pembaca awam (makin mirip
konten asli/kredibel, makin tinggi harm-nya). Level harm BUKAN penilaian
soal seberapa "serius" topiknya, tapi soal potensi menyesatkan orang:

- Fakta: substansi/inti klaim (termasuk kesimpulan sebab-akibatnya kalau
  ada) didukung penuh oleh isi artikel.

- Satire atau Parodi [Harm Terendah]: tidak berniat menyakiti/menipu, tapi
  berpotensi membuat orang salah paham kalau dibaca lepas dari konteks
  aslinya.

- False Connection [Harm Rendah]: judul, visual, atau caption pada klaim
  tidak didukung/tidak sesuai dengan isi konten sebenarnya (pola clickbait)
  -- pembaca yang baca sampai isi lengkap masih bisa menyadari
  ketidaksesuaiannya.

- Misleading Content [Harm Rendah-Sedang]: informasi digunakan secara
  menyesatkan untuk membingkai suatu isu atau individu -- lewat pemenggalan
  kutipan, statistik yang dipilih secara bias, atau framing yang mengubah
  makna asli -- lebih sulit disadari karena sebagian informasinya genuine.

- False Context [Harm Sedang]: konten (foto/video/kejadian) yang genuine
  disebarkan bersama informasi konteks yang salah -- mis. foto/video asli
  diklaim terjadi di tempat/waktu/situasi yang berbeda dari aslinya --
  meyakinkan karena materinya benar-benar asli, cuma konteksnya dipalsukan.

- Imposter Content [Harm Sedang-Tinggi]: sumber genuine (logo media, nama
  jurnalis, institusi, tokoh publik) dipalsukan/ditiru untuk membuat klaim
  palsu terlihat kredibel -- memanfaatkan kepercayaan orang pada nama besar,
  sehingga pembaca cenderung percaya tanpa cek lebih lanjut.

- Manipulated Content [Harm Tinggi]: informasi atau imagery genuine
  dimanipulasi secara teknis untuk menipu -- video/audio diedit,
  dipercepat/diperlambat, atau gambar digabungkan/di-crop secara menipu --
  butuh keahlian teknis untuk mendeteksi, jadi lebih sulit dibantah pembaca
  awam.

- Fabricated Content [Harm Tertinggi]: konten yang 100% baru dan palsu,
  tidak berdasar dari kejadian nyata manapun, dirancang sepenuhnya dan
  sengaja untuk menipu -- tidak ada unsur kebenaran sama sekali sebagai
  "jangkar" untuk memverifikasi, sehingga potensi kerugiannya paling besar

Jawab HANYA JSON dengan urutan field PERSIS seperti ini -- "alasan" WAJIB
ditulis LEBIH DULU sebelum "klasifikasi", supaya kesimpulanmu konsisten
dengan reasoning yang kamu tulis, bukan sebaliknya:
{{"alasan": "...", "klasifikasi": "Fakta"/"Satire atau Parodi"/"False Connection"/"Misleading Content"/"False Context"/"Imposter Content"/"Manipulated Content"/"Fabricated Content"}}"""