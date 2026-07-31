from app.services.groq_stance_service import URUTAN_TIE_BREAK


def _cari_kandidat_menang(breakdown: dict) -> list:
    skor_tertinggi = max(breakdown.values()) 
    return [kategori for kategori, jumlah in breakdown.items() if jumlah == skor_tertinggi] # mengambil kategori dengan vote terbanyak


def tentukan_klasifikasi_akhir_dengan_gambar(
    stance_breakdown: dict,
    alasan_per_artikel: list,
    detail_gambar_per_artikel: list
) -> str:
    """
    Majority vote teks seperti biasa. Kalau ada seri, tie-break pakai
    SIMILARITY GAMBAR TERTINGGI di antara kategori yang seri (match by url).
    Fallback ke URUTAN_TIE_BREAK statis kalau similarity juga tidak memutus seri.
    """
    kandidat = _cari_kandidat_menang(stance_breakdown)
    if len(kandidat) == 1:
        return kandidat[0]

    similarity_by_url = {
        d.get("url"): d.get("relevance_score", 0.0)
        for d in detail_gambar_per_artikel
    }

    skor_similarity_per_kategori = {}
    for kategori in kandidat:
        skor_terbaik = 0.0
        for artikel in alasan_per_artikel:
            if artikel.get("stance") == kategori:
                sim = similarity_by_url.get(artikel.get("url"), 0.0)
                skor_terbaik = max(skor_terbaik, sim)
        skor_similarity_per_kategori[kategori] = skor_terbaik

    skor_tertinggi = max(skor_similarity_per_kategori.values())
    kandidat_setelah_gambar = [k for k, v in skor_similarity_per_kategori.items() if v == skor_tertinggi]

    if len(kandidat_setelah_gambar) == 1:
        return kandidat_setelah_gambar[0]

    for kategori in URUTAN_TIE_BREAK:
        if kategori in kandidat_setelah_gambar:
            return kategori
    return kandidat_setelah_gambar[0]