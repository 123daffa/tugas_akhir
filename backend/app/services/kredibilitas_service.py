from app.core.constants import TAVILY_MAX_RESULTS

def calculate_kredibilitas_score(tavily_results: list) -> dict:

    if not tavily_results:
        return {
            "kredibilitas_score": 0.0,
            "jumlah_artikel": 0,
            "rata_rata_score": 0.0,
            "score_tertinggi": 0.0,
            "score_terendah": 0.0
        }

    scores = [article.get("score", 0.0) for article in tavily_results]

    jumlah_artikel = len(scores)
    rata_rata_score = sum(scores) / jumlah_artikel
    score_tertinggi = max(scores)
    score_terendah = min(scores)

    # Bobot jumlah artikel yang ditemukan
    bobot_jumlah = min(jumlah_artikel / TAVILY_MAX_RESULTS, 1.0) # Pastikan bobot tidak melebihi 1.0

    # 70% rata-rata score + 30% bobot jumlah artikel
    kredibilitas_score = (rata_rata_score * 0.7) + (bobot_jumlah * 0.3)
    kredibilitas_score = round(min(max(kredibilitas_score, 0.0), 1.0), 4) # Pastikan score berada di antara 0.0 dan 1.0

    print(f"[INFO] Kredibilitas score: {kredibilitas_score} dari {jumlah_artikel} artikel")

    return {
        "kredibilitas_score": kredibilitas_score,
        "jumlah_artikel": jumlah_artikel,
        "rata_rata_score": round(rata_rata_score, 4),
        "score_tertinggi": round(score_tertinggi, 4),
        "score_terendah": round(score_terendah, 4)
    }