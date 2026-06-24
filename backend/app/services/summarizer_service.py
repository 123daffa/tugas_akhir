import re
import torch
import torch.nn.functional as F
from app.models.indobert_model import indobert_handler

# Daftar stopword sederhana Bahasa Indonesia (kata yang tidak penting untuk query)
STOPWORDS = {
    "yang", "di", "ke", "dari", "ini", "itu", "dan", "atau", "dengan",
    "untuk", "pada", "adalah", "akan", "telah", "sudah", "juga", "saja",
    "dapat", "bisa", "tidak", "tersebut", "karena", "oleh", "sebagai",
    "dalam", "yaitu", "bahwa", "para", "sebuah", "suatu", "para", "lebih"
}

def clean_and_tokenize(text: str) -> list[str]:
    """Bersihkan teks dan pecah jadi kata-kata, buang stopword."""
    text = re.sub(r"[^\w\s]", "", text.lower())  # hapus tanda baca
    words = text.split()
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    return words

def extract_keywords(text: str, top_k: int = 5) -> str:
    """
    Ekstrak kata-kata paling penting dari teks menggunakan IndoBERT embedding similarity.
    Hasil dipakai sebagai query untuk Tavily Search.
    """
    words = clean_and_tokenize(text)
    
    if len(words) == 0:
        return text  # fallback kalau teks terlalu pendek/semua stopword
    
    if len(words) <= top_k:
        return " ".join(words)  # kalau kata sudah sedikit, tidak perlu filter lagi
    
    # Embedding untuk keseluruhan kalimat (representasi makna global)
    full_text_embedding = indobert_handler.get_embedding(text)
    
    # Embedding untuk tiap kata, lalu hitung similarity ke makna global
    word_scores = []
    for word in set(words):  # set() biar tidak hitung kata duplikat berulang
        word_embedding = indobert_handler.get_embedding(word)
        similarity = F.cosine_similarity(
            full_text_embedding.unsqueeze(0),
            word_embedding.unsqueeze(0)
        ).item()
        word_scores.append((word, similarity))
    
    # Urutkan berdasarkan similarity tertinggi, ambil top_k
    word_scores.sort(key=lambda x: x[1], reverse=True)
    top_words = [word for word, score in word_scores[:top_k]]
    
    query = " ".join(top_words)
    return query


def summarize_caption(text: str, top_k: int = 10) -> str:
    """Entry point yang dipanggil oleh pipeline."""
    return extract_keywords(text, top_k=top_k)