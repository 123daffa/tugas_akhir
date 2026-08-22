import time
import requests
from tavily import TavilyClient
from app.core.constants import TAVILY_MAX_RESULTS, TAVILY_SEARCH_DEPTH, TAVILY_TOPIC, TAVILY_EXCLUDE_DOMAINS
from app.core.config import settings

tavily_client = TavilyClient(settings.TAVILY_API_KEY)

# Konfigurasi retry -- cuma dipakai buat error jaringan sesaat (timeout/connection
# error), bukan buat error lain seperti API key salah atau quota habis (retry
# tidak akan membantu kasus itu, malah buang-buang waktu user).
TAVILY_MAX_RETRIES = 3
TAVILY_RETRY_BASE_DELAY = 2  # detik, dikali 2 tiap percobaan gagal (2s, 4s, 8s...)

# Error jaringan yang layak di-retry (koneksi putus sesaat, DNS gagal
# sementara, timeout). Di luar ini (mis. API key salah, quota habis,
# response tidak valid) langsung gagal tanpa retry.
TAVILY_RETRYABLE_ERRORS = (requests.exceptions.Timeout, requests.exceptions.ConnectionError)


def search_related_news_gambar(query: str, include_images: bool = False) -> dict:
    for attempt in range(1, TAVILY_MAX_RETRIES + 1):
        try:
            response = tavily_client.search(
                query=query,
                topic=TAVILY_TOPIC,
                search_depth=TAVILY_SEARCH_DEPTH,
                max_results=TAVILY_MAX_RESULTS,
                exclude_domains=TAVILY_EXCLUDE_DOMAINS,
                include_images=include_images
            )
            results = response.get("results", [])
            print(f"[INFO] Tavily menemukan {len(results)} artikel untuk query: '{query}'")
            for article in results:
                print(f"  - {article.get('title')} {article.get('content')} ({article.get('url')}) | Score: {article.get('score')}")
            return {"articles": results}

        except TAVILY_RETRYABLE_ERRORS as e:
            if attempt < TAVILY_MAX_RETRIES:
                delay = TAVILY_RETRY_BASE_DELAY * (2 ** (attempt - 1))
                print(f"[WARNING] Tavily search gagal (percobaan {attempt}/{TAVILY_MAX_RETRIES}) "
                      f"karena masalah jaringan: {e}. Coba lagi dalam {delay}s...")
                time.sleep(delay)
            else:
                print(f"[ERROR] Tavily search gagal setelah {TAVILY_MAX_RETRIES} percobaan "
                      f"(masalah jaringan): {e}")
                return {"articles": []}

        except Exception as e:
            print(f"[ERROR] Terjadi kesalahan saat mencari berita terkait: {e}")
            return {"articles": []}

    return {"articles": []}


def extract_images_from_articles(articles: list) -> list:
    """
    Ambil URL dari artikel-artikel TERPILIH (setelah filter kredibilitas,
    maks 5), lalu panggil Tavily Extract API (include_images=True) untuk
    mendapatkan gambar lengkap dari tiap halaman -- lebih hemat daripada
    include_images=True di tahap search awal, karena cuma dipanggil untuk
    artikel yang benar-benar dipakai, bukan semua hasil pencarian.
    """
    urls = [a.get("url") for a in articles if a.get("url")]
    if not urls:
        return articles

    for attempt in range(1, TAVILY_MAX_RETRIES + 1):
        try:
            response = tavily_client.extract(
                urls=urls,
                include_images=True,
                extract_depth="basic"
            )
            extracted_by_url = {r["url"]: r for r in response.get("results", [])}

            for gagal in response.get("failed_results", []):
                print(f"[WARNING] Gagal extract gambar dari {gagal.get('url')}: {gagal.get('error')}")

            for article in articles:
                hasil_extract = extracted_by_url.get(article.get("url"))
                article["images"] = hasil_extract.get("images", []) if hasil_extract else []

            return articles

        except TAVILY_RETRYABLE_ERRORS as e:
            if attempt < TAVILY_MAX_RETRIES:
                delay = TAVILY_RETRY_BASE_DELAY * (2 ** (attempt - 1))
                print(f"[WARNING] Tavily extract gagal (percobaan {attempt}/{TAVILY_MAX_RETRIES}) "
                      f"karena masalah jaringan: {e}. Coba lagi dalam {delay}s...")
                time.sleep(delay)
            else:
                print(f"[ERROR] Tavily extract gagal setelah {TAVILY_MAX_RETRIES} percobaan "
                      f"(masalah jaringan): {e}")
                for article in articles:
                    article.setdefault("images", [])
                return articles

        except Exception as e:
            print(f"[ERROR] Gagal extract gambar via Tavily: {e}")
            for article in articles:
                article.setdefault("images", [])
            return articles

    for article in articles:
        article.setdefault("images", [])
    return articles