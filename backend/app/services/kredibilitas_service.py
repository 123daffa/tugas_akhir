from app.core.constants import MINIMAL_SCORES_TAVILY

def calculate_score(tavily_results: list) -> dict:
    if not tavily_results:
        return {
            "selected_articles": [],
            "score_tavily": 0.0,
            "jumlah_artikel": 0,
        }

    # Urutkan berdasarkan score tertinggi
    sorted_results = sorted(
        tavily_results,
        key=lambda article: article.get("score", 0.0),
        reverse=True
    )

    # Ambil top 5 teratas, TAPI cuma yang score-nya > MINIMAL_SCORES_TAVILY
    # (bukan lagi "top 5 + tambahan di luar top 5", karena itu keponcotong
    # gara-gara [:5] di akhir -- sekarang jadi filter langsung di dalam top 5)
    selected_articles = [
        article for article in sorted_results[:5]
        # if article.get("score", 0.0) > MINIMAL_SCORES_TAVILY
    ]

    selected_scores = [article.get("score", 0.0) for article in selected_articles]

    jumlah_artikel = len(tavily_results)  # tetap jumlah SEMUA artikel
    score_tavily = sum(selected_scores) / len(selected_scores) if selected_scores else 0.0

    print(f"[INFO] Score: {score_tavily} dari {len(selected_scores)} artikel terpilih (total {jumlah_artikel} artikel)")

    return {
        "selected_articles": selected_articles,
        "score_tavily": score_tavily,
        "jumlah_artikel": jumlah_artikel,
    }