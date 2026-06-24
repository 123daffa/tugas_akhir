# from app.services.summarizer_service import summarize_caption
# from app.services.similarity_service import calculate_image_text_similarity
# from app.services.search_service import search_related_news
# from app.services.groq_service import get_kredibilitas_score, classify_content

# async def run_image_pipeline(image_bytes: bytes, caption: str) -> dict:
#     # Step 1: Hitung similarity CLIP
#     similarity_score = calculate_image_text_similarity(image_bytes, caption)
    
#     # Step 2: Summarize caption jadi query
#     query_text = summarize_caption(caption)
    
#     # Step 3: Cari berita terkait via Tavily
#     berita = await search_related_news(query_text)
    
#     # Step 4: Groq hitung kredibilitas dari berita
#     kredibilitas_score = await get_kredibilitas_score(berita, caption)
    
#     # Step 5: Klasifikasi akhir
#     hasil = classify_content(similarity_score, kredibilitas_score)
    
#     return {
#         "similarity_score": similarity_score,
#         "kredibilitas_score": kredibilitas_score,
#         "klasifikasi": hasil
#     }