from app.services.clip_service import encode_frames, compute_video_similarity_from_embeddings
from app.core.constants import CLIP_SIMILARITY_FLOOR, CLIP_SIMILARITY_CEILING


def _normalize_to_percentage(raw_similarity: float) -> float:
    """Sama seperti versi image_similarity_service -- skala cosine similarity
    CLIP mentah ke 0-100 supaya kompatibel dengan frontend (progress bar, dsb)."""
    span = CLIP_SIMILARITY_CEILING - CLIP_SIMILARITY_FLOOR
    normalized = (raw_similarity - CLIP_SIMILARITY_FLOOR) / span * 100
    return round(max(0.0, min(100.0, normalized)), 2)


def verify_video_relevance_per_artikel(frames: list, selected_articles: list) -> dict:
    """
    Similarity SEMUA FRAME video vs gambar tiap artikel, MURNI CLIP (lokal).
    Weighted aggregate by skor kredibilitas Tavily -- pola sama persis dengan
    image_similarity_service.verify_image_relevance_per_artikel. Embedding
    frame dihitung SEKALI (encode_frames), dipakai ulang untuk semua artikel.
    """
    weighted_score = 0.0
    total_weight = 0.0
    detail_per_artikel = []

    print(f"[INFO] Encode {len(frames)} frame video (sekali saja, dipakai untuk semua artikel)...")
    frame_embeddings = encode_frames(frames)

    for article in selected_articles:
        gambar_artikel = article.get("images", [])
        if not gambar_artikel:
            continue

        print(f"[INFO] Cek gambar artikel: {article.get('title', 'Tanpa judul')} ({len(gambar_artikel)} gambar kandidat)")
        raw_similarity = compute_video_similarity_from_embeddings(frame_embeddings, gambar_artikel)
        skor_persen = _normalize_to_percentage(raw_similarity)
        weight = article.get("score", 0.5)

        weighted_score += skor_persen * weight
        total_weight += weight

        detail_per_artikel.append({
            "judul": article.get("title", "Tanpa judul"),
            "url": article.get("url", "#"),
            "relevance_score": skor_persen,
            "penjelasan": f"Skor kemiripan visual (frame video paling mirip) dengan gambar dari artikel ini: {skor_persen:.1f}%."
        })

    print("[INFO] Selesai hitung similarity video.")

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