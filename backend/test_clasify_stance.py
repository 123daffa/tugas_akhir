"""
Test manual untuk classify_text_by_stance (dan vote_single_article_stance).
Jalankan di environment lokal kamu (yang sudah punya GROQ_API_KEY valid di .env).

Cara pakai:
    python test_classify_stance.py
"""

import json
from app.services.groq_stance_service import (
    classify_text_by_stance,
    vote_single_article_stance,
)

# ---------------------------------------------------------------------------
# Data uji: klaim + artikel asli dari log kamu (gempa Kumamoto, 8 artikel Tavily)
# ---------------------------------------------------------------------------

CLAIM = (
    "Gempa dengan kekuatan M 7,1 mengguncang Kumamoto, Pulau Kyushu, Jepang, "
    "memakan korban jiwa. Dilaporkan satu orang tewas dan 50 orang mengalami luka-luka."
)

ARTICLES = [
    {
        "title": "A magnitude 7.1 earthquake shakes part of southern Japan but no tsunami detected",
        "url": "https://www.sfchronicle.com/news/world/article/a-magnitude-7-1-earthquake-shakes-part-of-22362982.php",
        "content": "A magnitude 7.1 earthquake shook southern Japan on Tuesday, causing damage to buildings and injuring several people, officials said. No tsunami was detected following the quake.",
        "score": 0.72254705,
    },
    {
        "title": "Japan: Magnitude 7.1 earthquake in Kyushu leaves several injured, damages buildings",
        "url": "https://www.bbc.com/news/articles/clyer9mdjz7o",
        "content": "A powerful earthquake struck Japan's Kyushu region, leaving several people injured and damaging buildings. Authorities are assessing the full extent of the damage.",
        "score": 0.7187726,
    },
    {
        "title": "Major earthquake rocks Japan, prompting tsunami warnings",
        "url": "https://www.nbcnews.com/world/japan/earthquake-rocks-japan-tsunami-warnings-rcna589574",
        "content": "A major earthquake rocked Japan on Tuesday, prompting tsunami warnings for coastal areas. Residents were urged to evacuate to higher ground as a precaution.",
        "score": 0.69672287,
    },
    {
        "title": "7.1 Magnitude Earthquake Hits Japan's Kyushu Region",
        "url": "https://www.huffpost.com/entry/major-earthquake-hits-japan_n_6a6867c3e4b02c67a5adc7af",
        "content": "A 7.1 magnitude earthquake hit Japan's Kyushu region, causing widespread disruption. Emergency services are responding to reports of injuries and structural damage.",
        "score": 0.68748367,
    },
    {
        "title": "A magnitude 7.1 earthquake shakes part of southern Japan and a tsunami advisory is issued",
        "url": "https://www.washingtonpost.com/world/2026/07/28/japan-earthquake-tsunami/",
        "content": "A magnitude 7.1 earthquake shook southern Japan, and a tsunami advisory was issued for parts of the coastline. Officials reported injuries and damage to infrastructure.",
        "score": 0.6685563,
    },
]


def test_single_vote():
    print("=" * 70)
    print("TEST 1: vote_single_article_stance (satu artikel)")
    print("=" * 70)

    article = ARTICLES[0]
    result = vote_single_article_stance(CLAIM, article)

    print(f"Artikel : {article['title']}")
    print(f"Hasil   : {json.dumps(result, indent=2, ensure_ascii=False)}")

    assert "stance" in result, "Response harus punya field 'stance'"
    assert result["stance"] in ("MENDUKUNG", "MEMBANTAH", "TIDAK_RELEVAN"), \
        f"Stance tidak valid: {result['stance']}"

    print("[PASS] Struktur response valid\n")


def test_full_classification():
    print("=" * 70)
    print("TEST 2: classify_text_by_stance (5 artikel, full pipeline)")
    print("=" * 70)

    result = classify_text_by_stance(CLAIM, ARTICLES)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    assert result["klasifikasi"] in ("Fakta", "Hoaks"), \
        f"Klasifikasi tidak valid: {result['klasifikasi']}"
    assert 0.0 <= result["confidence_score"] <= 1.0, \
        f"Confidence di luar rentang 0-1: {result['confidence_score']}"
    assert len(result["alasan_per_artikel"]) == len(ARTICLES[:5]), \
        "Jumlah alasan per artikel tidak sesuai jumlah artikel yang diproses"

    print(f"\n[INFO] Klaim ini FAKTUAL (berdasarkan berita asli BBC/NBC/dst),")
    print(f"[INFO] jadi ekspektasi hasil idealnya: klasifikasi == 'Fakta'")
    print(f"[INFO] Hasil aktual: klasifikasi == '{result['klasifikasi']}'")

    if result["klasifikasi"] != "Fakta":
        print("[WARNING] Hasil tidak sesuai ekspektasi — cek 'alasan_per_artikel' di atas")
    else:
        print("[PASS] Sesuai ekspektasi")


def test_empty_articles():
    print("=" * 70)
    print("TEST 3: classify_text_by_stance dengan artikel kosong")
    print("=" * 70)

    result = classify_text_by_stance(CLAIM, [])
    print(json.dumps(result, indent=2, ensure_ascii=False))

    assert result["klasifikasi"] == "Hoaks", "Artikel kosong harus fallback ke Hoaks"
    assert result["confidence_score"] == 0.0
    print("[PASS] Fallback artikel kosong sesuai\n")


if __name__ == "__main__":
    test_single_vote()
    test_full_classification()
    test_empty_articles()
    print("\nSemua test selesai dijalankan.")