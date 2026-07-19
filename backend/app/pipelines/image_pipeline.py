from app.models.translator_model import translator_handler
from app.models.clip_model import clip_handler
from app.services.groq_service import summarize_tavily_results
from app.services.search_service import search_related_news
from app.services.kredibilitas_service import calculate_kredibilitas_score
from app.services.classification_service import classify_content
from PIL import Image
import io

def ensure_url(url: str) -> str:
    if not url:
        return '#'
    if not url.startswith(('http://', 'https://')):
        return f'https://{url}'
    return url

def run_image_pipeline(image_bytes: bytes, caption: str) -> dict:
    # Step 1: Buka gambar
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Step 2: Translasi caption ke Inggris
    caption_en = translator_handler.translate(caption)

    # Step 3: Hitung CLIP similarity
    similarity_score = clip_handler.get_similarity(image, caption_en)

    # Step 4: Tavily cari berita
    berita = search_related_news(caption)

    # Step 5: Hitung kredibilitas dari metadata Tavily
    kredibilitas_data = calculate_kredibilitas_score(berita)

    # Step 6: Groq summarize → penjelasan untuk user
    penjelasan = summarize_tavily_results(berita, caption)

    # Step 7: Klasifikasi akhir
    klasifikasi = classify_content(
        similarity_score,
        kredibilitas_data["kredibilitas_score"]
    )

    return {
        "similarity_score": round(similarity_score, 4), 
        "caption_translated": caption_en,
        "jumlah_artikel": kredibilitas_data["jumlah_artikel"],
        "kredibilitas_score": kredibilitas_data["kredibilitas_score"],
        "penjelasan": penjelasan,
        "klasifikasi": klasifikasi,
        "articles": [                          
            {
                "title": a.get("title", "Tanpa judul"),
                "url": ensure_url(a.get("url", "")),
                "score": round(a.get("score", 0.0), 4)
            }
            for a in berita
        ]
    }