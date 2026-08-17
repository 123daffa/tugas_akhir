from app.services.groq_stance_service import URUTAN_TIE_BREAK


def tentukan_klasifikasi_akhir_dengan_gambar(
    stance_breakdown: dict,
    alasan_per_artikel: list,
    detail_gambar_per_artikel: list
) -> str:
    """
    Klasifikasi akhir ditentukan oleh artikel dengan relevance_score
    gambar PALING TINGGI di antara SEMUA artikel (tanpa memandang
    stance-nya menang vote atau tidak) -- stance artikel tersebut
    yang dipakai sebagai hasil akhir.

    Fallback ke majority vote teks (+ URUTAN_TIE_BREAK) HANYA kalau
    tidak ada data gambar sama sekali, atau semua relevance_score-nya 0.
    """
    similarity_by_url = {
        d.get("url"): d.get("relevance_score", 0.0)
        for d in detail_gambar_per_artikel
    }

    artikel_dengan_stance = [
        artikel for artikel in alasan_per_artikel
        if artikel.get("stance")
    ]

    if artikel_dengan_stance:
        artikel_terbaik = max(
            artikel_dengan_stance,
            key=lambda a: similarity_by_url.get(a.get("url"), 0.0)
        )
        skor_terbaik = similarity_by_url.get(artikel_terbaik.get("url"), 0.0)

        if skor_terbaik > 0.0:
            return artikel_terbaik.get("stance")

    # Fallback: tidak ada info gambar yang bisa dipakai
    skor_tertinggi = max(stance_breakdown.values())
    kandidat = [k for k, v in stance_breakdown.items() if v == skor_tertinggi]

    if len(kandidat) == 1:
        return kandidat[0]

    for kategori in URUTAN_TIE_BREAK:
        if kategori in kandidat:
            return kategori
    return kandidat[0]