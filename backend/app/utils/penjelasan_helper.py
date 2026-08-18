def build_penjelasan(stance_result: dict) -> str:
    """
    Rakit penjelasan singkat dari hasil majority vote 8 kategori.
    """
    breakdown = stance_result["stance_breakdown"]
    total_artikel = len(stance_result["alasan_per_artikel"])

    if total_artikel == 0:
        return "Tidak ditemukan artikel berita terkait untuk memverifikasi klaim ini."

    if klasifikasi_final is None:
        klasifikasi_final = stance_result["klasifikasi"]

    rincian = ", ".join(f"{jumlah} artikel {kategori}" for kategori, jumlah in breakdown.items() if jumlah > 0)

    return (
        f"Berdasarkan analisis {total_artikel} artikel berita ({rincian}), "
        f"kesimpulan: {klasifikasi_final}."
    )