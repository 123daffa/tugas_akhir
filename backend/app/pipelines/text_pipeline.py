from app.services.summarizer_service import summarize_caption
# from app.services.search_service import search_related_news
# from app.services.groq_service import get_kredibilitas_score, classify_content_text_only

# async def run_text_pipeline(text: str) -> dict:
#     # Tidak ada CLIP similarity karena tidak ada gambar
#     query_text = summarize_caption(text)
#     berita = await search_related_news(query_text)
#     kredibilitas_score = await get_kredibilitas_score(berita, text)
#     hasil = classify_content_text_only(kredibilitas_score)  # logic klasifikasi beda (cuma 2 kategori: fakta/false)
    
#     return {
#         "kredibilitas_score": kredibilitas_score,
#         "klasifikasi": hasil
#     }