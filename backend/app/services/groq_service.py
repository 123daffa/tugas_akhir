from groq import Groq
from app.core.config import settings
from app.core.constants import GROQ_MODEL_NAME

groq_client = Groq(api_key=settings.GROQ_API_KEY)


def summarize_tavily_results(tavily_results: list, original_text: str) -> str:
    """
    Groq merangkum artikel hasil Tavily menjadi penjelasan singkat untuk user.
    Pakai model kecil (8B instant) karena task lebih sederhana dan butuh response cepat.
    """
    if not tavily_results:
        return "Tidak ditemukan artikel berita terkait untuk dianalisis."

    articles_text = ""
    for i, article in enumerate(tavily_results[:5], 1): # 
        title = article.get("title", "Tanpa judul")
        content = article.get("content", "")[:300]
        articles_text += f"\nArtikel {i}:\nJudul: {title}\nIsi: {content}\n"

    prompt = f"""Kamu adalah asisten fact-checking. Berikan ringkasan singkat dari artikel berikut yang berkaitan dengan klaim yang diperiksa.

KLAIM:
{original_text}

ARTIKEL:
{articles_text}

Tulis ringkasan 2-3 kalimat Bahasa Indonesia yang:
- Menjelaskan apa yang ditemukan di artikel terkait
- Menyebutkan apakah artikel mendukung atau membantah klaim
- Mudah dipahami pembaca awam

Tulis langsung tanpa preamble apapun."""

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[ERROR] Groq summarize Tavily gagal: {e}")
        return "Gagal merangkum artikel terkait."