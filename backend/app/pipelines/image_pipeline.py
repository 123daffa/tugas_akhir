from app.services.search_service_gambar import search_related_news_gambar
from app.services.kredibilitas_service import calculate_kredibilitas_score
from app.services.groq_stance_service import classify_text_by_stance
from app.services.groq_vision_service import verify_image_relevance_per_artikel
from app.utils.penjelasan_helper import build_penjelasan
from app.core.constants import IMAGE_RELEVANCE_THRESHOLD


def _combine_stance_and_image(stance_klasifikasi: str, image_relevance_score: float) -> str:
    """
    Gabungkan stance teks (Fakta / False Content) + relevansi gambar (0-100)
    menjadi salah satu dari 4 kategori resmi:
    Fakta, Misleading Content, Fabricated Content, False Content.
    """
    gambar_relevan = image_relevance_score >= IMAGE_RELEVANCE_THRESHOLD
    if stance_klasifikasi == "Fakta":
        return "Fakta" if gambar_relevan else "Misleading Content"
    else:  # stance_klasifikasi == "False Content"
        return "Fabricated Content" if gambar_relevan else "False Content"


def run_image_pipeline(image_url: str, caption: str) -> dict:
    # Step 1: Tavily cari berita, tiap artikel bawa gambarnya sendiri
    hasil_tavily = search_related_news_gambar(caption, include_images=True)
    berita = hasil_tavily["articles"]

    # Step 2: Kredibilitas + artikel terpilih
    kredibilitas_data = calculate_kredibilitas_score(berita)
    selected_articles = kredibilitas_data.get("selected_articles", [])

    # Step 3: Stance teks (per artikel, weighted by Tavily score)
    stance_result = classify_text_by_stance(caption, selected_articles)

    # Step 4: Relevansi gambar (per artikel, weighted by Tavily score juga)
    image_result = verify_image_relevance_per_artikel(image_url, caption, selected_articles)

    # Step 5: Gabungkan jadi klasifikasi akhir 4 kategori
    klasifikasi_akhir = _combine_stance_and_image(
        stance_result["klasifikasi"],
        image_result["relevance_score"]
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
            {
                "title": a.get("title", "Tanpa judul"),
                "url": a.get("url", "#"),
                "score": round(a.get("score", 0.0), 4)
            }
            for a in berita
        ]
    }