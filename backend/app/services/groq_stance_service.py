import json
from groq import Groq
from app.core.config import settings
from app.core.constants import GROQ_MODEL_NAME

groq_client = Groq(api_key=settings.GROQ_API_KEY)


def vote_single_article_stance(claim: str, article: dict) -> dict:
    """Tentukan SIKAP satu artikel (pakai snippet Tavily, field 'content')
    terhadap klaim -- dinilai SATU artikel per panggilan, bukan gabungan
    5 sekaligus, supaya keputusan lebih longgar/tidak 'terlalu ketat'."""
    title = article.get("title", "Tanpa judul")
    snippet = article.get("content", "")[:500] # maks 500 karakter

    prompt = f"""Kamu adalah asisten fact-checking. Tentukan sikap artikel ini
terhadap klaim berikut.

KLAIM: {claim}

ARTIKEL:
Judul: {title}
Cuplikan: {snippet}

Pilih SATU sikap:
- MENDUKUNG: artikel ini membenarkan/mendukung klaim
- MEMBANTAH: artikel ini bertentangan/membantah klaim
- TIDAK_RELEVAN: artikel ini tidak benar-benar membahas klaim ini

Jawab HANYA JSON: {{"stance": "MENDUKUNG"/"MEMBANTAH"/"TIDAK_RELEVAN", "alasan": "..."}}"""

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=200,
            response_format={"type": "json_object"} # parsing input ke json
        )
        return json.loads(response.choices[0].message.content) # diparsing 
    except Exception as e:
        print(f"[WARNING] Gagal vote stance 1 artikel: {e}")
        return {"stance": "TIDAK_RELEVAN", "alasan": "Gagal dianalisis"}


def classify_text_by_stance(claim: str, selected_articles: list) -> dict:
    """Klasifikasi BINARY (Fakta/Hoaks) berdasarkan voting stance berbobot
    skor Tavily dari maksimal 5 artikel teratas.

    Aturan: kalau total bobot MENDUKUNG > total bobot (MEMBANTAH + TIDAK_RELEVAN)
    -> Fakta. Selain itu -> Hoaks.
    """
    
    if not selected_articles: # kalau enggak ada langsung dianggap False
        return {
            "klasifikasi": "False Content",
            "confidence_score": 0.0,
            "stance_breakdown": {"MENDUKUNG": 0, "MEMBANTAH": 0, "TIDAK_RELEVAN": 0},
            "alasan_per_artikel": []
        }

    weighted_stance = {"MENDUKUNG": 0.0, "MEMBANTAH": 0.0, "TIDAK_RELEVAN": 0.0}
    total_weight = 0.0
    alasan_list = []

    for article in selected_articles: # melakukan looping untuk mengecek artikel 
        vote = vote_single_article_stance(claim, article)
        stance = vote.get("stance", "TIDAK_RELEVAN")
        if stance not in weighted_stance:
            stance = "TIDAK_RELEVAN"

        weight = article.get("score", 0.5)
        weighted_stance[stance] += weight
        total_weight += weight

        alasan_list.append({
            "judul": article.get("title", "Tanpa judul"),
            "stance": stance,
            "alasan": vote.get("alasan", "")
        })

    if total_weight == 0:
        return {
            "klasifikasi": "False Content", "confidence_score": 0.0,
            "stance_breakdown": weighted_stance, "alasan_per_artikel": alasan_list
        }

    dukung = weighted_stance["MENDUKUNG"]
    lainnya = total_weight - dukung
    confidence = round(dukung / total_weight, 4)

    if dukung > lainnya and confidence >= 0.70:
        klasifikasi = "Fakta" 
    else:
        klasifikasi = "False Content"
        
    return {
        "klasifikasi": klasifikasi,
        "confidence_score": confidence,
        "stance_breakdown": weighted_stance,
        "alasan_per_artikel": alasan_list
    }