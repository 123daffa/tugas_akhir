// Data dummy -- nanti diganti hasil fetch dari backend Flask, misalnya:
// GET /api/history          -> daftar riwayat (dipakai RiwayatView.vue)
// GET /api/history/:id      -> detail 1 item (dipakai RiwayatDetailView.vue)
//
// Sengaja ditaruh di 1 file terpisah (bukan langsung di dalam view) supaya
// RiwayatView.vue (daftar) dan RiwayatDetailView.vue (detail) bisa
// "berbagi" sumber data yang sama tanpa duplikasi.
export const historyItems = [
  {
    id: 1,
    image: '',
    category: 'Fakta',
    date: '10 Okt 2024',
    type: 'Teks',
    title: 'Pernyataan Resmi Pemerintah Terkait Bantuan Sosial Tahap Baru',
    verified: true,
    accuracy: 92,
    conclusion:
      'Klaim mengenai penyaluran bantuan sosial tahap baru ini sesuai dengan pengumuman resmi yang dikeluarkan oleh Kementerian Sosial melalui kanal resminya. Tidak ditemukan indikasi manipulasi konteks maupun distorsi informasi.',
    source: {
      title: 'Siaran Pers Resmi Kementerian Sosial RI',
      url: 'https://kemensos.go.id'
    },
    metrics: [
      { label: 'Manipulasi Konteks', value: 8, color: 'red' },
      { label: 'Bahasa Emosional', value: 12, color: 'orange' }
    ]
  },
  {
    id: 2,
    image: '',
    category: 'False Content',
    date: '12 Okt 2024',
    type: 'Gambar',
    title: 'Klaim Vaksin Generasi Baru Mengandung Cip Pelacak',
    verified: true,
    accuracy: 96,
    conclusion:
      'Klaim ini sepenuhnya tidak berdasar. Tidak ada bukti ilmiah maupun regulasi resmi yang mendukung keberadaan cip pelacak dalam vaksin. Gambar yang beredar merupakan hasil manipulasi digital dari foto vial vaksin asli.',
    source: {
      title: 'Klarifikasi Resmi Badan POM RI',
      url: 'https://pom.go.id'
    },
    metrics: [
      { label: 'Manipulasi Konteks', value: 91, color: 'red' },
      { label: 'Bahasa Emosional', value: 84, color: 'orange' }
    ]
  },
  {
    id: 3,
    image: '',
    category: 'Misleading Content',
    date: '08 Okt 2024',
    type: 'Video',
    title: 'Video Editan Pidato Calon Pemimpin Daerah Disebarkan Tanpa Konteks',
    verified: true,
    accuracy: 85,
    conclusion:
      'Video ini merupakan potongan asli dari pidato yang sebenarnya, namun disebarkan tanpa konteks pertanyaan/pernyataan sebelumnya, sehingga menimbulkan kesan yang berbeda dari maksud aslinya.',
    source: {
      title: 'Rekaman Lengkap Acara oleh Media Lokal',
      url: '#'
    },
    metrics: [
      { label: 'Manipulasi Konteks', value: 78, color: 'red' },
      { label: 'Bahasa Emosional', value: 65, color: 'orange' }
    ]
  },
  {
    id: 4,
    image: '',
    category: 'Fabricated Content',
    date: '08 Okt 2024',
    type: 'Video',
    title: 'Video Editan Pidato Calon Pemimpin Daerah Versi Kedua yang Beredar',
    verified: true,
    accuracy: 90,
    conclusion:
      'Audio pada video telah dimodifikasi menggunakan teknik sinkronisasi suara buatan (voice cloning) untuk mengubah sebagian isi pernyataan. Analisis spektrum audio menunjukkan anomali pada pola suara asli narasumber.',
    source: {
      title: 'Analisis Forensik Digital oleh Tim Ahli Independen',
      url: '#'
    },
    metrics: [
      { label: 'Manipulasi Konteks', value: 88, color: 'red' },
      { label: 'Bahasa Emosional', value: 72, color: 'orange' }
    ]
  }
]

/**
 * Cari 1 item riwayat berdasarkan id.
 * @param {string|number} id
 */
export function findHistoryById(id) {
  // route params selalu berupa string, sedangkan id di data ini number,
  // makanya dibandingkan pakai == bukan === -- ATAU dikonversi eksplisit,
  // di sini saya pilih konversi eksplisit biar lebih jelas maksudnya.
  return historyItems.find((item) => item.id === Number(id))
}