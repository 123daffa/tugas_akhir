from app.services.frame_extraction_service import extract_keyframes
from app.services.search_service_gambar import search_related_news_gambar, extract_images_from_articles
from app.services.kredibilitas_service import calculate_kredibilitas_score
from app.services.groq_stance_gambar_service import classify_text_by_stance
from app.services.video_similarity_service import verify_video_relevance_per_artikel
from app.services.klasifikasi_gabungan_service import tentukan_klasifikasi_akhir_dengan_gambar
from app.utils.penjelasan_helper import build_penjelasan
from app.utils.url_helper import ensure_url

def run_video_pipeline(video_bytes: bytes, caption: str) -> dict:
    # Step 1: Ekstrak frame dari video (langkah TAMBAHAN dibanding image pipeline)
    frames = extract_keyframes(video_bytes)
    
   # Step 2: Tavily search TANPA gambar (lebih hemat credit, gambar diambil
    # ulang lebih lengkap khusus untuk artikel terpilih di Step 2.5)
    hasil_tavily = search_related_news_gambar(caption, include_images=False)
    berita = hasil_tavily["articles"]
   
    # Step 3: Kredibilitas + artikel terpilih (maks 5)
    kredibilitas_data = calculate_kredibilitas_score(berita)
    selected_articles = kredibilitas_data.get("selected_articles", [])

    # Step 3.5: Extract gambar lengkap khusus untuk artikel terpilih (Tavily Extract API)
    selected_articles = extract_images_from_articles(selected_articles)

    # Step 4: # Klasifikasi teks menggunakan majority vote 4 kategori
    stance_result = classify_text_by_stance(caption, selected_articles)

    # Step 5: Similarity frame -- CLIP saja, tanpa Groq sama sekali
    video_result = verify_video_relevance_per_artikel(frames, selected_articles)

    # Step 6: Gabungkan jadi klasifikasi akhir 4 kategori
    klasifikasi_akhir = tentukan_klasifikasi_akhir_dengan_gambar(
        stance_result["stance_breakdown"],
        stance_result["alasan_per_artikel"],
        video_result["detail_per_artikel"]
    )
    
    return {
        "jumlah_frame": len(frames),
        "jumlah_artikel": kredibilitas_data["jumlah_artikel"],
        "kredibilitas_score": kredibilitas_data["kredibilitas_score"],
        "klasifikasi": klasifikasi_akhir,
        "confidence": stance_result["confidence_score"] * 100,
        "video_relevance_score": video_result["relevance_score"],
        "penjelasan_teks": build_penjelasan(stance_result),
        "penjelasan_video": video_result["penjelasan"],
        "artikel_video_paling_relevan": video_result.get("artikel_paling_relevan"),   # ← BARIS BARU
        "stance_breakdown": stance_result["stance_breakdown"],
        "alasan_per_artikel": stance_result["alasan_per_artikel"],
        "detail_video_per_artikel": video_result["detail_per_artikel"],
        "articles": [
            {
                "title": a.get("title", "Tanpa Judul"),
                "url": ensure_url(a.get("url", "")),
                "score": round(a.get("score", 0.0), 4)
            }
            for a in berita
        ],
        "_first_frame": frames[0] if frames else None,
    }