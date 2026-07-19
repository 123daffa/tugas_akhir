def calculate_kredibilitas_score(tavily_results: list) -> dict:

    if not tavily_results:
        return {
            "jumlah_artikel": 0,
        }

    scores = [article.get("score", 0.0) for article in tavily_results]

    jumlah_artikel = len(scores)
    kredibilitas_score = sum(scores) / jumlah_artikel
    

    print(f"[INFO] Kredibilitas score: {kredibilitas_score} dari {jumlah_artikel} artikel")

    return {
        "kredibilitas_score": kredibilitas_score,
        "jumlah_artikel": jumlah_artikel,
    }