def build_penjelasan(stance_result: dict) -> str:
    """
    Rakit penjelasan singkat dari hasil voting stance,
    karena classify_text_by_stance tidak menghasilkan penjelasan naratif siap pakai.
    """
    breakdown = stance_result["stance_breakdown"]
    total_artikel = len(stance_result["alasan_per_artikel"])
    dukung = breakdown.get("MENDUKUNG", 0)
    bantah = breakdown.get("MEMBANTAH", 0)
    tidak_relevan = breakdown.get("TIDAK_RELEVAN", 0)

    if total_artikel == 0:
        return "Tidak ditemukan artikel berita terkait untuk memverifikasi klaim ini."

    return (
        f"Berdasarkan analisis {total_artikel} artikel berita, "
        f"{dukung:.2f} bobot skor mendukung klaim ini, "
        f"{bantah:.2f} membantah, dan {tidak_relevan:.2f} tidak relevan. "
        f"Kesimpulan: {stance_result['klasifikasi']}."
    )