# from app.services.frame_extraction_service import extract_keyframes
# from app.services.summarizer_service import summarize_caption
# from app.services.similarity_service import calculate_image_text_similarity
# from app.services.search_service import search_related_news
# from app.services.groq_service import get_kredibilitas_score, classify_content

# def ensure_url(url: str) -> str:
#     """Pastikan URL selalu punya prefix https://"""
#     if not url:
#         return '#'
#     if not url.startswith(('http://', 'https://')):
#         return f'https://{url}'
#     return url

# async def run_video_pipeline(video_bytes: bytes, caption: str) -> dict:
#     # Step 1: Ekstrak frame dari video (langkah TAMBAHAN dibanding image pipeline)
#     frames = extract_keyframes(video_bytes)
    
#     # Step 2: Hitung similarity rata-rata dari semua frame
#     similarity_scores = [
#         calculate_image_text_similarity(frame, caption) 
#         for frame in frames
#     ]
#     similarity_score = sum(similarity_scores) / len(similarity_scores)
    
#     # Step 3-5: SAMA seperti image_pipeline (reuse service yang sama!)
#     query_text = summarize_caption(caption)
#     berita = await search_related_news(query_text)
#     kredibilitas_score = await get_kredibilitas_score(berita, caption)
#     hasil = classify_content(similarity_score, kredibilitas_score)
    
#     return {
#         "similarity_score": similarity_score,
#         "kredibilitas_score": kredibilitas_score,
#         "klasifikasi": hasil,
#         "jumlah_frame_dianalisis": len(frames),
#     }