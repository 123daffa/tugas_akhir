from app.services.search_service import search_related_news
from app.services.classification_service import classify_text_only

async def run_text_pipeline(text: str) -> dict:

    # Step 1: Tavily cari berita terkait
    berita = await search_related_news(text)

    # Step 2: Klasifikasi (teks saja = hanya 2 kemungkinan: FAKTA atau FALSE)
    klasifikasi = classify_text_only(berita)

    return {
        "query_used": text,
        "kredibilitas_score": kredibilitas_score,
        "klasifikasi": klasifikasi
    }