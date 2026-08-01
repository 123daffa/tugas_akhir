from app.services.search_service_gambar import search_related_news_gambar, extract_images_from_articles
from app.services.kredibilitas_service import calculate_kredibilitas_score
from app.services.groq_stance_gambar_service import classify_text_by_stance
from app.services.image_similarity_service import verify_image_relevance_per_artikel
from app.services.klasifikasi_gabungan_service import tentukan_klasifikasi_akhir_dengan_gambar
from app.utils.penjelasan_helper import build_penjelasan
from app.utils.url_helper import ensure_url

def ensure_url(url: str) -> str:
    """Pastikan URL selalu punya prefix https://"""
    if not url:
        return '#'
    if not url.startswith(('http://', 'https://')):
        return f'https://{url}'
    return url

def run_image_pipeline(image_url: str, caption: str) -> dict:
    # Step 1: Tavily search TANPA gambar (lebih hemat credit, gambar diambil
    # ulang lebih lengkap khusus untuk artikel terpilih di Step 2.5)
    hasil_tavily = search_related_news_gambar(caption, include_images=False)
    berita = hasil_tavily["articles"]

    # Step 2: Kredibilitas + artikel terpilih (maks 5)
    kredibilitas_data = calculate_kredibilitas_score(berita)
    selected_articles = kredibilitas_data.get("selected_articles", [])

    # Step 2.5: Extract gambar lengkap khusus untuk artikel terpilih (Tavily Extract API)
    selected_articles = extract_images_from_articles(selected_articles)

    # Step 3: Stance teks (majority/weighted vote, tidak berubah)
    stance_result = classify_text_by_stance(caption, selected_articles)

    # Step 4: Similarity gambar -- CLIP saja, tanpa Groq sama sekali
    image_result = verify_image_relevance_per_artikel(image_url, selected_articles)

    # Step 5: Gabungkan jadi klasifikasi akhir 4 kategori
    klasifikasi_akhir = tentukan_klasifikasi_akhir_dengan_gambar(
        stance_result["stance_breakdown"],
        stance_result["alasan_per_artikel"],
        image_result["detail_per_artikel"]
    )

    return {
        "jumlah_artikel": kredibilitas_data["jumlah_artikel"],
        "kredibilitas_score": kredibilitas_data["kredibilitas_score"],
        "klasifikasi": klasifikasi_akhir,
        "confidence": stance_result["confidence_score"] * 100,
        "image_relevance_score": image_result["relevance_score"],
        "penjelasan_teks": build_penjelasan(stance_result),
        "penjelasan_gambar": image_result["penjelasan"],
        "artikel_gambar_paling_relevan": image_result.get("artikel_paling_relevan"),
        "stance_breakdown": stance_result["stance_breakdown"],
        "alasan_per_artikel": stance_result["alasan_per_artikel"],
        "detail_gambar_per_artikel": image_result["detail_per_artikel"],
        "articles": [
            {"title": a.get("title", "Tanpa judul"), 
             "url": ensure_url(a.get("url", "")),
             "score": round(a.get("score", 0.0), 4)}
            for a in berita
        ]
    }