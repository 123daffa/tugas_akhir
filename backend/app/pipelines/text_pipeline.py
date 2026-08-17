from app.services.search_service import search_related_news
from app.services.kredibilitas_service import calculate_score
from app.services.groq_stance_service import classify_text_by_stance
from app.utils.penjelasan_helper import build_penjelasan
from app.utils.url_helper import ensure_url

def run_text_pipeline(caption: str) -> dict:

    # Step 1: Tavily cari berita
    berita = search_related_news(caption)

    # Step 2: Hitung kredibilitas dari metadata Tavily + selected articles
    data_tavily = calculate_score(berita)
    selected_articles = data_tavily.get("selected_articles", [])

    # Step 3: Groq summarize artikel → penjelasan untuk user + klasifikasi
    stance_result = classify_text_by_stance(caption, selected_articles)
    
    return {
        "jumlah_artikel": data_tavily["jumlah_artikel"],
        "score_tavily": data_tavily["score_tavily"],
        "klasifikasi": stance_result["klasifikasi"],
        "confidence": round(stance_result["confidence_score"] * 100, 2),  # 0-1 -> 0-100
        "penjelasan": build_penjelasan(stance_result),
        "alasan_per_artikel": stance_result["alasan_per_artikel"],
        "stance_breakdown": stance_result["stance_breakdown"],
        "articles": [
            {
                "title": a.get("title", "Tanpa judul"),
                "url": ensure_url(a.get("url", "")),   
                "score": round(a.get("score", 0.0), 4)
            }
            for a in berita
        ]
    }