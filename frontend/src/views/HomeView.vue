<script setup>
import {
  CheckCircle2,
  Laugh,
  Link2,
  Clock,
  MapPinOff,
  Drama,
  Scissors,
  AlertTriangle
} from 'lucide-vue-next'
</script>

<template>
  <section id="landing">
    <div class="home">
    <ul class="home-features">
      <li class="home-feature-list"> 🔴Pemeriksa Fakta berbahasa Indonesia, bertenaga AI</li>
    </ul>
    <h1 class="home-title">Periksa Kebenaran</h1>
    <h1 class="home-subtitle">dengan tenang.</h1>
    <p class="home-paragraf">Tempelkan klaim, kutipan berita, atau pesan berantai. Kami bantu telusuri
      konteks, sebutkan ketidakpastian, dan ajak Anda berpikir jernih. Sistem deteksi
      berita multimodal berbasis AI. Kami menganalisis teks, gambar, dan video
      untuk memberikan klarifikasi yang transparan dan akurat.</p>
      <div class="btn-group">
          <RouterLink to="/deteksi" class="btn-mulai">Mulai Periksa Klaim</RouterLink>
          <!-- <RouterLink to="/tentang" class="btn-tentang">Bagaimana cara kerjanya?</RouterLink> -->
      </div>
      <div class="home-claim">
        <ul class="home-claim-list">
          <li class="home-claim-pill home-claim-fakta">Fakta</li>
          <li class="home-claim-pill home-claim-satire">Satire atau Parodi</li>
          <li class="home-claim-pill home-claim-false-connection">False Connection</li>
          <li class="home-claim-pill home-claim-misleading">Misleading Content</li>
          <li class="home-claim-pill home-claim-false-context">False Context</li>
          <li class="home-claim-pill home-claim-imposter">Imposter Content</li>
          <li class="home-claim-pill home-claim-manipulated">Manipulated Content</li>
          <li class="home-claim-pill home-claim-fabricated">Fabricated Content</li>
        </ul>
      </div>  
    </div>
  </section>

  <section id="keunggulan">
    <div class="keunggulan-header">
      <h1>Mengapa 
        <span>FactCheck.ID</span>?
      </h1>
      <h3>Platform deteksi berita hoaks berbasis AI yang mengombinasikan analisis semantic similarity dengan pengecekan kredibilitas sumber menggunakan Tavily Search untuk mendukung proses verifikasi informasi secara cepat dan terpercaya.</h3>
    </div>

    <div class="keunggulan-grid">
      <!-- Kartu teknologi mesin pencarian -->
      <div class="keunggulan-stat-card">
        <div class="keunggulan-stat-image">
          <img src="../assets/default-thumbnail-home.jpeg" alt="Foto Fact Check ID" />
        </div>

        <div class="keunggulan-stat-body">
          <h2> Teknologi Mesin Pencarian</h2>
          <p class="keunggulan-stat-desc">
            Menggunakan <span class="keunggulan-highlight">Tavily Search </span>, salah satu platform yang memungkinkan AI agent mengakses web secara aman dan terukur. 
            Tavily menyediakan pencarian real-time, scraping, dan pengambilan data terstruktur dalam satu API call — 
            dirancang khusus untuk LLM dan AI agent.
          </p>
          <ul class="keunggulan-tags">
            <li>CLIP</li>
            <li>Open CV</li> 
            <li>Tavily Search</li>
            <li>Groq AI</li>
          </ul>
        </div>
      </div>

      <!-- Kartu keunggulan sistem -->
      <div class="keunggulan-info-list">
        <div class="keunggulan-info-card">
          <div class="keunggulan-info-icon keunggulan-icon-teal">⚡</div>
          <div class="keunggulan-info-content">
            <h4>Deteksi Realtime</h4>
            <p>Analisis klaim, gambar, maupun video diproses secara langsung dalam hitungan detik, sehingga pengguna bisa langsung mengambil keputusan tanpa menunggu verifikasi manual.</p>
          </div>
        </div>

        <div class="keunggulan-info-card">
          <div class="keunggulan-info-icon keunggulan-icon-slate">⊞</div>
          <div class="keunggulan-info-content">
            <h4>Multiclass Classification</h4>
            <p>Setiap konten diklasifikasikan ke dalam empat kategori spesifik — Fakta, False, Misleading, dan Fabricated — bukan sekadar benar atau salah, sehingga konteksnya lebih jelas.</p>
          </div>
        </div>

        <div class="keunggulan-info-card">
          <div class="keunggulan-info-icon keunggulan-icon-green">🌐</div>
          <div class="keunggulan-info-content">
            <h4>Verifikasi Berbasis Sumber</h4>
            <p>Sistem membandingkan informasi dengan sumber berita dan referensi terpercaya untuk meningkatkan keakuratan proses verifikasi.</p>
          </div>
        </div>

        <div class="keunggulan-info-card">
          <div class="keunggulan-info-icon keunggulan-icon-green">🧩</div>
          <div class="keunggulan-info-content">
            <h4>Deteksi Multimodal</h4>
            <p>Satu sistem yang mampu menganalisis teks, gambar, dan video sekaligus, sehingga klaim yang disertai konten visual pun tetap bisa diverifikasi secara menyeluruh.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section id="kategori-deteksi">
    <div class="kategori-deteksi-header">
      <h1>Multiclass Clasification</h1>
      <h3>Sistem kami mengklasifikasikan informasi ke dalam empat kategori utama untuk
          memberikan konteks yang jelas pada setiap berita.</h3>
    </div>
    <div class="kategori-penjelasan">
    <div class="kategori-item-fakta">
      <CheckCircle2 :size="40" class="kategori-icon" />
      <h2>Fakta</h2>
      <p>Informasi yang telah diverifikasi kebenarannya melalui pengecekan silang dengan sumber-sumber terpercaya, data resmi, dan bukti pendukung yang dapat diverifikasi. Konten dalam kategori ini telah melewati proses analisis dan tidak mengandung unsur manipulasi.</p>
    </div>

    <div class="kategori-item-satire">
      <Laugh :size="40" class="kategori-icon" />
      <h2>Satire atau Parodi</h2>
      <p>Konten yang dibuat sebagai lelucon atau sindiran tanpa niat menyesatkan atau merugikan siapa pun. Meski begitu, konten ini tetap berpotensi membuat pembaca salah paham dan menganggapnya serius apabila dibaca tanpa memahami konteks aslinya.</p>
    </div>

    <div class="kategori-item-false-connection">
      <Link2 :size="40" class="kategori-icon" />
      <h2>False Connection</h2>
      <p>Informasi di mana judul, gambar, atau keterangan (caption) tidak sesuai atau tidak didukung oleh isi konten sebenarnya. Pola ini sering ditemukan pada judul clickbait yang dibuat sensasional demi menarik perhatian pembaca.</p>
    </div>

    <div class="kategori-item-misleading">
      <Clock :size="40" class="kategori-icon" />
      <h2>Misleading Content</h2>
      <p>Informasi yang disajikan dengan cara yang menyesatkan meskipun mengandung elemen kebenaran di dalamnya. Biasanya berupa fakta yang dipelintir, diambil di luar konteks, atau disajikan sebagian saja sehingga menimbulkan kesan atau kesimpulan yang keliru bagi pembaca.</p>
    </div>

    <div class="kategori-item-false-context">
      <MapPinOff :size="40" class="kategori-icon" />
      <h2>False Context</h2>
      <p>Konten asli (foto, video, atau peristiwa nyata) yang disebarluaskan bersama keterangan waktu, tempat, atau situasi yang salah. Materinya benar-benar asli, namun konteks yang menyertainya telah diputarbalikkan.</p>
    </div>

    <div class="kategori-item-imposter">
      <Drama :size="40" class="kategori-icon" />
      <h2>Imposter Content</h2>
      <p>Informasi yang mengatasnamakan atau meniru sumber terpercaya, seperti logo media resmi, nama jurnalis, atau institusi tertentu, padahal sumber tersebut tidak pernah mengeluarkan pernyataan tersebut. Bertujuan membuat klaim palsu terlihat lebih kredibel.</p>
    </div>

    <div class="kategori-item-manipulated">
      <Scissors :size="40" class="kategori-icon" />
      <h2>Manipulated Content</h2>
      <p>Informasi yang telah terbukti dipalsukan atau dimodifikasi dari sumber aslinya, baik melalui manipulasi gambar/video, pengeditan kutipan, atau penyuntingan konten resmi. Biasanya disebarkan dengan tujuan tertentu, seperti menyudutkan pihak tertentu atau menciptakan kepanikan.</p>
    </div>

    <div class="kategori-item-fabricated">
      <AlertTriangle :size="40" class="kategori-icon" />
      <h2>Fabricated Content</h2>
      <p>Informasi yang sepenuhnya dibuat tanpa dasar fakta sama sekali, mulai dari klaim, angka, hingga peristiwa yang digambarkan. Konten jenis ini biasanya diciptakan untuk tujuan manipulasi opini publik, penipuan, atau sekadar hiburan yang menyesatkan pembaca.</p>
    </div>
  </div>
  </section>

  <section id="teknologi">
    <div class="teknologi-header">
      <h1>Teknologi yang Digunakan</h1>
      <h3>Dibangun dengan teknologi terkini untuk kecepatan dan akurasi maksimal.</h3>
    </div>
 
    <div class="teknologi-grid">
      <div class="teknologi-item">
        <h4 class="kategori-teknologi">Frontend</h4>
         <div class="teknologi-icon"><img src="../assets/vue.svg" alt="Logu Vue"></div>
        <h4>Vue.js</h4>
        <p>Frontend reaktif &amp; dinamis</p>
      </div>
 
      <div class="teknologi-item">
        <h4 class="kategori-teknologi">Backend</h4>
        <div class="teknologi-icon"><img src="../assets/flask.svg" alt="Logo Flask"></div>
        <h4>Flask</h4>
        <p>Backend berkinerja tinggi</p>
      </div>
 
      <div class="teknologi-item">
        <h4 class="kategori-teknologi">Database</h4>
        <div class="teknologi-icon"><img src="../assets/supabase.svg" alt="Logo Supabase"></div>
        <h4>Supabase</h4>
        <p>Database real-time terkelola</p>
      </div>
 
      <div class="teknologi-item">
        <h4 class="kategori-teknologi">AI Inference</h4>
        <div class="teknologi-icon"><img src="../assets/groq.png" alt="Logo Groq"></div>
        <h4>Groq LLM</h4>
        <p>Inferensi AI super cepat</p>
      </div>
    </div>

    <div class="teknologi-grid-2">
      <div class="teknologi-item">
        <h4 class="kategori-teknologi">Computer Vision</h4>
        <div class="teknologi-icon"><img src="../assets/huggingface.svg" alt="Logo Hugging Face"></div>
        <h4>Clip</h4>
        <p>Analisis kesamaan gambar-gambar</p>
      </div>

       <div class="teknologi-item">
        <h4 class="kategori-teknologi">Search Engine</h4>
        <div class="teknologi-icon"><img src="../assets/tavily.svg" alt="Logo Tavily"></div>
        <h4>Tavily Search</h4>
        <p>Pencarian informasi real-time</p>
      </div>

    </div>
  </section>
</template>

<style scoped>
section {
  padding: 64px 128px;
}

.home {
  text-align: center;
}

#landing {
  align-items: center;
  margin-top: 30px;
}
.home-features {
  list-style-type: none;
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.home-feature-list {
  width: fit-content;
  background-color: white;
  border: 2px solid #808080;
  color: black;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 14px;
}
h1 {
  margin: 0;
  line-height: 1.2;
  padding-bottom: 5px;
}
.home-title {
  font-weight: bold;
  font-size: 65px;
  color: black;
}
.home-subtitle {
  font-weight: bold;
  font-size: 65px;
  background: linear-gradient(
      90deg,
      #4f6677 0%,
      #2f8f8b 45%,
      #20d48a 100%
    );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  }
.home-paragraf { 
  max-width: 900px;
  font-size: 18px;
  line-height: 1.4;
  text-align: center;
  margin: 30px auto 0;
  padding: 5px 100px;
}

.btn-group {
  margin-top: 30px;
  font-size: 15px;
  margin-bottom: 80px;
}

.btn-mulai {
  margin-right: 50px;
  background-color: #1B2B4B;
  padding: 10px 35px;
  border: 2px solid ;
  color: white;
  border-radius: 50px;
}

.btn-tentang {
  background-color: white;
  padding: 10px 30px;
  border: 2px solid #808080;
  color: black;
  border-radius: 50px;
}

.home-claim-list {
  margin-top: 60px;
  list-style-type: none;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
  margin-bottom: 40px;
  padding: 0;
}

/* Style dasar dipisah ke satu class shared, tinggal tambah modifier
   warna per kategori -- menggantikan 4 (sekarang 8) blok copy-paste. */
.home-claim-pill {
  padding: 10px 22px;
  border-radius: 20px;
  color: white;
  font-size: 14px;
  font-weight: 500;
}

/* Warna diurutkan dari low harm ke high harm, mengikuti spektrum
   "7 Types of Mis- and Disinformation" (First Draft, Claire Wardle 2019),
   senada dengan warna badge di ResultCard.vue dan HistoryCard.vue */
.home-claim-fakta {
  background-color: #20d48a;
}

.home-claim-satire {
  background-color: #4dd0c4;
}

.home-claim-false-connection {
  background-color: #ffe066;
  color: #333;
}

.home-claim-misleading {
  background-color: #ffcc00;
}

.home-claim-false-context {
  background-color: #ff9933;
}

.home-claim-imposter {
  background-color: #ff704d;
}

.home-claim-manipulated {
  background-color: #ff4d4d;
}

.home-claim-fabricated {
  background-color: #808080;
}

#keunggulan {
background-color: #EFF4FF;
}

.keunggulan-header {
  text-align: center;
  line-height: 1.4;
  max-width: 60%;
  margin: 50px auto 60px;
  color: black;
}

.keunggulan-header h1 {
  font-weight: 600;
  font-size: 50px;
}

.keunggulan-header span {
  font-weight: bold;
  font-size: 60px;
  background: linear-gradient(
      90deg,
      #4f6677 0%,
      #2f8f8b 45%,
      #20d48a 100%
    );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
.keunggulan-header h3 {
  font-size: 20px;
  margin-top: 20px;
  font-weight: 400;
  color: black;
}

.keunggulan-grid {
  display: flex;
  align-items: stretch;
  gap: 40px;
  margin-bottom: 40px;
}

@media (max-width: 900px) {
  .keunggulan-grid {
    flex-direction: column;
  }
}

/* ===== Kartu teknologi mesin pencarian (kiri) ===== */
.keunggulan-stat-card {
  flex: 1;
  background-color: rgba(251, 252, 251, 0.7);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.keunggulan-stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.keunggulan-stat-image {
  aspect-ratio: 2 / 1.5;      /* rasio kotak container, biar konsisten sama card lain */
  overflow: hidden;           /* WAJIB -- biar bagian gambar yang "kelebihan" ke-crop, bukan meluber */
  background-color: #EFF4FF;
  border-radius: 20px 20px 0 0;  /* rounded cuma di atas, biar nyambung sama card di bawahnya */
}

.keunggulan-stat-image img {
  /* width: 100%;
  height: 100%; */
  object-fit: cover;          /* INI KUNCINYA -- gambar di-scale & di-crop biar ngisi penuh tanpa gepeng */
  display: block;
  text-align: center;
  justify-content: center;
}
.keunggulan-stat-body {
  padding: 30px;
  text-align: left;
}

.keunggulan-stat-body h2 {
  font-size: 25px;
  font-weight: 700;
  margin: 0 0 10px;
  color: black;
}

.keunggulan-stat-desc {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
  margin: 0 0 16px;
}

.keunggulan-highlight {
  color: #20d48a;
  font-weight: 600;
}

.keunggulan-tags {
  list-style-type: none;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0;
  padding: 0;
}

.keunggulan-tags li {
  background-color: rgba(32, 212, 138, 0.12);
  color: #1a9c6c;
  font-size: 14px;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 20px;
}

/* ===== Kartu keunggulan sistem (kanan) ===== */
.keunggulan-info-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.keunggulan-info-card {
  flex: 1;
  background-color: rgba(251, 252, 251, 0.7);
  border-radius: 20px;
  padding: 24px;
  display: flex;
  gap: 16px;
  text-align: left;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.keunggulan-info-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.keunggulan-info-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
}

/* Warna icon disamakan dengan gradient di .home-subtitle (#4f6677 -> #2f8f8b -> #20d48a)
   biar 3 kartu keunggulan ini terasa satu keluarga warna dengan identitas brand */
.keunggulan-icon-teal {
  background-color: rgba(47, 143, 139, 0.12);
  color: #2f8f8b;
}

.keunggulan-icon-slate {
  background-color: rgba(79, 102, 119, 0.12);
  color: #4f6677;
}

.keunggulan-icon-green {
  background-color: rgba(32, 212, 138, 0.12);
  color: #20d48a;
}

.keunggulan-info-content h4 {
  font-size: 25px;
  font-weight: 700;
  margin: 0 0 6px;
  color: black;
}

.keunggulan-info-content p {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
  margin: 0;
}

#kategori-deteksi {
  background-color: white;
}

.kategori-deteksi-header {
  text-align: center;
  line-height: 1.4;
  max-width: 60%;
  margin: 50px auto 100px;
  color: black;
}

.kategori-deteksi-header h1 {
  font-weight: 700;
}

.kategori-deteksi-header h3 {
  margin-top: 20px;
  color: #666;
}

/* Diganti dari flex ke grid -- flex 8 item sejajar akan terlalu sempit,
   grid bisa wrap otomatis ke beberapa baris sesuai lebar layar. */
.kategori-penjelasan {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  align-items: stretch;
  margin-top: 50px;
  padding: 0 20px;
  gap: 30px;
}

@media (max-width: 1100px) {
  .kategori-penjelasan {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 560px) {
  .kategori-penjelasan {
    grid-template-columns: 1fr;
  }
}

/* Icon lucide (component), menggantikan selector "img" lama */
.kategori-icon {
  display: block;
  margin: 0 auto 20px;
}

.kategori-penjelasan h2 {
  text-align: center;
  font-size: 18px;
  margin-bottom: 10px;
}

.kategori-penjelasan p {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

/* Satu class shared untuk semua kartu kategori -- menggantikan 4 blok
   copy-paste identik sebelumnya. Tinggal tambah class ini + modifier
   warna di setiap div kategori. */
[class^="kategori-item-"] {
  background-color: rgba(251, 252, 251, 0.7);
  color: black;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

[class^="kategori-item-"]:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

/* Warna icon tiap kategori, mengikuti spektrum low->high harm
   (First Draft, Claire Wardle 2019) -- senada dengan warna badge
   di ResultCard.vue dan HistoryCard.vue */
.kategori-item-fakta .kategori-icon {
  color: #20d48a;
}

.kategori-item-satire .kategori-icon {
  color: #4dd0c4;
}

.kategori-item-false-connection .kategori-icon {
  color: #e0b800;
}

.kategori-item-misleading .kategori-icon {
  color: #ffcc00;
}

.kategori-item-false-context .kategori-icon {
  color: #ff9933;
}

.kategori-item-imposter .kategori-icon {
  color: #ff704d;
}

.kategori-item-manipulated .kategori-icon {
  color: #ff4d4d;
}

.kategori-item-fabricated .kategori-icon {
  color: #808080;
}


#teknologi {
  background-color: #EFF4FF;
}
 
.teknologi-header {
  text-align: center;
  line-height: 1.4;
  max-width: 60%;
  margin: 0 auto 50px;
  color: black;
}
 
.teknologi-header h1 {
  font-weight: 700;
  font-size: 30px;
}
 
.teknologi-header h3 {
  margin-top: 12px;
  font-weight: 400;
  font-size: 18px;
  color: #555;
}
 
.teknologi-grid {
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  gap: 24px;
}
 
@media (max-width: 900px) {
  .teknologi-grid {
    flex-wrap: wrap;
  }
}
 
.teknologi-item {
  flex: 1;
  min-width: 180px;
  background-color: white;
  border-radius: 20px;
  padding: 32px 20px;
  text-align: center;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
 
.teknologi-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.kategori-teknologi {
  letter-spacing: 1px;
  font-weight: 600;
  background: linear-gradient(
      90deg,
      #4f6677 0%,
      #2f8f8b 45%,
      #20d48a 100%
    );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
 
.teknologi-icon {
  width: 120px;
  height: 100px;
  margin: 0 auto 16px;
  background-color: white;
  border: 1px solid #eee;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.teknologi-icon img {
  width: 80px;
  /* opacity: 0.5; */
}
 
.teknologi-item h4 {
  font-size: 22px;
  font-weight: 700;
  color: black;
  margin: 0 0 6px;
}
 
.teknologi-item p {
  font-size: 18px;
  color: #666;
  margin: 0;
}

.teknologi-grid-2 {
  margin-top: 50px;
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  gap: 24px;
}
</style>