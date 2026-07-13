from app.services.search_service import search_related_news
from app.services.kredibilitas_service import calculate_kredibilitas_score
from app.services.classification_service import classify_text_only

def run_text_pipeline(text: str) -> dict:

    # Step 1: Tavily cari berita
    berita = search_related_news(text)

    # Step 2: Hitung kredibilitas dari metadata Tavily
    kredibilitas_data = calculate_kredibilitas_score(berita)

    # # Step 3: Groq summarize artikel → penjelasan untuk user
    # penjelasan = summarize_tavily_results(berita, text)

    # Step 4: Klasifikasi
    klasifikasi = classify_text_only(kredibilitas_data["kredibilitas_score"])

    return {
        "jumlah_artikel": kredibilitas_data["jumlah_artikel"],
        "rata_rata_score": kredibilitas_data["rata_rata_score"],
        "kredibilitas_score": kredibilitas_data["kredibilitas_score"],
        # "penjelasan": penjelasan,
        "klasifikasi": klasifikasi
    }