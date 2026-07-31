from app.services.clip_service import compute_image_similarity

# Estimasi kalibrasi awal skala cosine similarity CLIP (BUKAN 0-1 intuitif).
# PERLU disesuaikan berdasarkan pengujian nyata dengan kasus gambar sungguhan.
CLIP_SIMILARITY_FLOOR = 0.45
CLIP_SIMILARITY_CEILING = 0.85


def _normalize_to_percentage(raw_similarity: float) -> float:
    """Ubah cosine similarity CLIP mentah jadi skala 0-100, untuk kompatibilitas
    dengan frontend yang sudah ada (progress bar, threshold, dsb)."""
    span = CLIP_SIMILARITY_CEILING - CLIP_SIMILARITY_FLOOR
    normalized = (raw_similarity - CLIP_SIMILARITY_FLOOR) / span * 100
    return round(max(0.0, min(100.0, normalized)), 2)


def verify_image_relevance_per_artikel(image_url: str, selected_articles: list) -> dict:
    """
    Similarity gambar user vs gambar tiap artikel, MURNI pakai CLIP (lokal,
    tanpa panggilan LLM/API eksternal sama sekali untuk gambar). Weighted
    aggregate by skor kredibilitas Tavily, pola sama seperti voting stance teks.
    """
    weighted_score = 0.0
    total_weight = 0.0
    detail_per_artikel = []

    print(f"[INFO] Mulai hitung similarity gambar (CLIP) untuk {len(selected_articles)} artikel...")

    for article in selected_articles:
        gambar_artikel = article.get("images", [])
        if not gambar_artikel:
            continue

        print(f"[INFO] Cek gambar artikel: {article.get('title', 'Tanpa judul')} ({len(gambar_artikel)} gambar kandidat)")
        raw_similarity = compute_image_similarity(image_url, gambar_artikel)
        skor_persen = _normalize_to_percentage(raw_similarity)
        weight = article.get("score", 0.5)

        weighted_score += skor_persen * weight
        total_weight += weight

        detail_per_artikel.append({
            "judul": article.get("title", "Tanpa judul"),
            "url": article.get("url", "#"),
            "relevance_score": skor_persen,
            "penjelasan": f"Skor kemiripan visual dengan gambar dari artikel ini: {skor_persen:.1f}%."
        })

    print("[INFO] Selesai hitung similarity gambar.")

    if total_weight == 0:
        return {
            "relevance_score": 0,
            "penjelasan": "Tidak ada artikel dengan gambar untuk dibandingkan.",
            "artikel_paling_relevan": None,
            "detail_per_artikel": []
        }

    skor_akhir = round(weighted_score / total_weight, 2)
    artikel_paling_relevan = max(detail_per_artikel, key=lambda x: x["relevance_score"])

    return {
        "relevance_score": skor_akhir,
        "penjelasan": artikel_paling_relevan["penjelasan"],
        "artikel_paling_relevan": artikel_paling_relevan["judul"],
        "detail_per_artikel": detail_per_artikel
    }