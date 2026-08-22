
def build_prompt_klasifikasi(claim: str, title: str, snippet: str) -> str:
    return f"""Kamu adalah asisten ai saya, kamu berperan sebagai senior fact checker 
  yang bertujuan untuk menentukan apakah klaim dibawah ini merupakan fakta atau hoaks.
  Fakta adalah substansi/inti klaim didukung penuh oleh isi artikel berdasarkan judul dan cuplikan.

  Bandingkan klaim dengan artikel.

  jika klaim adalah hoaks, klasifikasikan klaim ke salah satu dari 7 kategori hoaks berikut:

1. Fabricated Content: New content that is 100% false, designed to decieve and do harm

2. Manipulated Content: When genuine information or imagery is manipulated to decieve

3. Imposter Content: When genuine sources are impersonated

4. False Context: When genuine content is shared with false contextual information

5. Misleading Content: Misleading use of information to frame an issue or individual

6. False Connection: When headlines, visuals or captions don’t support the content.

7. Satire atau Parodi: No intention to cause harm but has potential to fool

klaim: {claim}

artikel:
judul: {title}
Cuplikan: {snippet}

PENTING -- perhatikan pola ini sebelum memutuskan, ikuti urutan prioritas berikut:

PRIORITAS 1 -- Sebelum menjawab, pastikan ALASAN yang kamu tulis konsisten
dengan kategori yang dipilih: merujuk ke artikel, dan
menyebut secara eksplisit CIRI dari kategori tersebut. jika pada artikel terdapat ciri eksplisit kategorikan klaim sesuai ciri tersebut.
contohnya kata manipulasi untuk kategori manipulated content, misleading untuk misleading content, dan konten tiruan/penipuan dan sebagainya,
sesuaikan kata tersebut dengan klasifikasi di atas. cek juga keterangan waktu klaim dan artikel apakah sesuai, kalau tidak ada waktu atau 
pembanding antara klaim dan artikel maka jangan langsung di anggap itu langsung fakta walau konteks sesuai.
dan jika tidak ada ciri eksplisit, jelaskan alasannya secara logis.

PRIORITAS 2 -- Kalau artikel mengandung tag DEBUNKING EKSPLISIT seperti
"[SALAH]", "[HOAKS]", "Cek Fakta:", "Keliru:", "Klarifikasi:", "Hoaks,"/"Hoaks:",
itu adalah VONIS bahwa SELURUH NARASI dalam klaim adalah hoaks. Cari kata kunci "kesimpulan".
fokus pada kata kunci tersebut.

PRIORITAS 3 -- Cek dulu apakah kejadian atau berita pada klaim itu benar terjadi sesuai artikel. jangan langsung 
memberikan pernyataan bahwa kejadian tersebut tidak benar. bisa saja kejadian tersebut ada tapi pada konteks yang berbeda.
jika hal itu terjadi teliti apakah artikel memberikan kategori salah satu dari 7 kategori hoaks diatas.

PRIORITAS 4 -- jika pada artikel terdapat kata "tidak didukung", "tidak disebutkan", "hoaks", atau berita tidak sesuai dengan klaim,
maka klasifikasi tidak boleh fakta

Jawab HANYA JSON dengan urutan field PERSIS seperti ini -- "alasan" WAJIB
ditulis LEBIH DULU sebelum "klasifikasi", supaya kesimpulanmu konsisten
dengan reasoning yang kamu tulis, bukan sebaliknya:
{{"alasan": "...", "klasifikasi": "Fakta"/"Satire atau Parodi"/"False Connection"/"Misleading Content"/"False Context"/"Imposter Content"/"Manipulated Content"/"Fabricated Content"}}"""