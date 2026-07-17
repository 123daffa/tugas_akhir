<script setup>
import PipelineNode from '../components/how_it_works/PipelineNode.vue'
import PipelineArrow from '../components/how_it_works/PipelineArrow.vue'
import ResultNode from '../components/how_it_works/ResultNode.vue'

// Data hasil klasifikasi akhir, sesuai 4 kategori di diagram kamu.
// Dipisah jadi array biar gampang di-loop & di-maintain (misal nanti nambah kategori baru)
const classifications = [
  {
    label: 'FAKTA',
    description: 'Similarity tinggi + kredibilitas score tinggi',
    tone: 'green'
  },
  {
    label: 'MISLEADING',
    description: 'Similarity rendah + kredibilitas tinggi',
    tone: 'orange'
  },
  {
    label: 'FABRICATED',
    description: 'Similarity tinggi + kredibilitas rendah',
    tone: 'red'
  },
  {
    label: 'FALSE',
    description: 'Similarity tinggi + kredibilitas sangat rendah',
    tone: 'pink'
  }
]
</script>

<template>
  <div class="how-it-works">
    <header class="page-header">
      <h1>Bagaimana Sistem Ini Bekerja</h1>
      <p>
        Alur pemrosesan sistem deteksi hoaks multimodal untuk mode Gambar + Teks,
        mulai dari input pengguna hingga klasifikasi akhir.
      </p>
    </header>

    <!-- ======================= TAHAP 1: PREPROCESSING ======================= -->
    <section class="stage">
      <h2 class="stage-title">1. Preprocessing Input</h2>
      <p class="stage-desc">
        Gambar dan teks klaim yang diunggah pengguna diubah ke representasi
        yang bisa diproses model, lalu diterjemahkan ke Bahasa Inggris
        (karena model CLIP dilatih pada data berbahasa Inggris).
      </p>
      <div class="row row--wrap">
        <PipelineNode title="Gambar + Teks" subtitle="Input dari pengguna" />
        <PipelineArrow />
        <PipelineNode title="Convert to Vector" subtitle="Embedding representation" />
        <PipelineArrow />
        <PipelineNode title="Translate to English" subtitle="Marian MT" />
      </div>
    </section>

    <!-- ======================= TAHAP 2: CLIP SIMILARITY (BERCABANG) ======================= -->
    <section class="stage">
      <h2 class="stage-title">2. Analisis Kemiripan Gambar & Teks (CLIP)</h2>
      <p class="stage-desc">
        Cosine Similarity antara embedding gambar dan teks dihitung menggunakan CLIP.
        Dari sini alurnya bercabang dua: skor kemiripan disimpan sebagai salah satu
        variabel penentu klasifikasi, sementara caption gambar dipakai untuk menyusun
        query pencarian fakta.
      </p>

      <div class="branch-layout">
        <div class="branch-main">
          <PipelineNode title="Cosine Similarity - CLIP" subtitle="Menghitung skor kemiripan" variant="output" />
        </div>

        <div class="branch-arrows">
          <PipelineArrow direction="vertical" />
        </div>

        <div class="branch-columns">
          <div class="branch-col">
            <PipelineNode title="Similarity Score" subtitle="Dipakai sebagai variabel klasifikasi" variant="output" />
          </div>
          <div class="branch-col">
            <PipelineNode title="Ambil Query dari Caption" subtitle="Ekstrak kata kunci dari hasil CLIP" />
          </div>
        </div>
      </div>
    </section>

    <!-- ======================= TAHAP 3: PENCARIAN FAKTA (TAVILY) ======================= -->
    <section class="stage">
      <h2 class="stage-title">3. Verifikasi Fakta via Pencarian Web</h2>
      <p class="stage-desc">
        Query hasil ekstraksi caption dicari menggunakan Tavily Search. Hasil pencarian
        menghasilkan dua hal sekaligus: kumpulan berita relevan sebagai bahan rujukan,
        dan skor kredibilitas berdasarkan metadata sumber (bukan isi berita).
      </p>
      <div class="row row--wrap">
        <PipelineNode title="Query Teks" />
        <PipelineArrow />
        <PipelineNode title="Tavily Search" subtitle="Pencarian web real-time" />
      </div>

      <div class="branch-layout branch-layout--secondary">
        <div class="branch-arrows">
          <PipelineArrow direction="vertical" />
        </div>
        <div class="branch-columns">
          <div class="branch-col">
            <PipelineNode title="Berita" subtitle="Artikel relevan yang ditemukan" />
          </div>
          <div class="branch-col">
            <PipelineNode title="Kredibilitas Score" subtitle="Dari metadata sumber Tavily" variant="output" />
          </div>
        </div>
      </div>
    </section>

    <!-- ======================= TAHAP 4: KLASIFIKASI GROQ ======================= -->
    <section class="stage">
      <h2 class="stage-title">4. Klasifikasi oleh Groq LLM</h2>
      <p class="stage-desc">
        Ketiga variabel — similarity score, berita hasil pencarian, dan skor kredibilitas —
        digabungkan dan dikirim ke Groq LLM untuk dianalisis dan diklasifikasikan
        ke dalam salah satu dari empat kategori berikut.
      </p>
      <div class="row row--wrap">
        <PipelineNode title="Groq LLM" subtitle="Menganalisis seluruh variabel" />
        <PipelineArrow />
        <PipelineNode title="Klasifikasi" variant="final" />
      </div>
    </section>

    <!-- ======================= TAHAP 5: HASIL AKHIR ======================= -->
    <section class="stage">
      <h2 class="stage-title">5. Hasil Klasifikasi</h2>
      <p class="stage-desc">
        Kombinasi tinggi/rendahnya similarity score dan kredibilitas score menentukan
        kategori akhir yang ditampilkan ke pengguna.
      </p>
      <div class="results-grid">
        <ResultNode
          v-for="item in classifications"
          :key="item.label"
          :label="item.label"
          :description="item.description"
          :tone="item.tone"
        />
      </div>
    </section>
  </div>
</template>

<style scoped>
.how-it-works {
  width: 100%;
}

.page-header {
  text-align: center;
  max-width: 640px;
  margin: 0 auto 48px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 800;
  color: var(--color-navy);
  margin: 0 0 12px;
}

.page-header p {
  font-size: 14px;
  color: var(--color-text-muted);
  line-height: 1.6;
  margin: 0;
}

.stage {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 28px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-card);
}

.stage-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-navy);
  margin: 0 0 8px;
}

.stage-desc {
  font-size: 13px;
  color: var(--color-text-muted);
  line-height: 1.6;
  margin: 0 0 20px;
  max-width: 720px;
}

.row {
  display: flex;
  align-items: center;
}

.row--wrap {
  flex-wrap: wrap;
  row-gap: 16px;
}

/* Layout percabangan: node utama di atas, panah vertikal di tengah,
   lalu 2 kolom hasil cabang berjejer di bawahnya */
.branch-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.branch-layout--secondary {
  margin-top: 4px;
}

.branch-main {
  display: flex;
  justify-content: center;
}

.branch-arrows {
  display: flex;
  justify-content: center;
}

.branch-columns {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  justify-content: center;
}

.branch-col {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

@media (max-width: 640px) {
  .row {
    flex-direction: column;
  }

  .row .arrow--horizontal {
    transform: rotate(90deg);
    min-width: 20px;
    margin: 4px 0;
  }
}
</style>