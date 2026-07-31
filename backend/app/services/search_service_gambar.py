from tavily import TavilyClient
from app.core.constants import TAVILY_MAX_RESULTS, TAVILY_SEARCH_DEPTH, TAVILY_TOPIC
from app.core.config import settings

tavily_client = TavilyClient(settings.TAVILY_API_KEY)


def search_related_news_gambar(query: str, include_images: bool = False) -> dict:
    try:
        response = tavily_client.search(
            query=query,
            topic=TAVILY_TOPIC,
            search_depth=TAVILY_SEARCH_DEPTH,
            max_results=TAVILY_MAX_RESULTS,
            include_images=include_images
        )
        results = response.get("results", [])
        print(f"[INFO] Tavily menemukan {len(results)} artikel untuk query: '{query}'")
        return {"articles": results}
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat mencari berita terkait: {e}")
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
    except Exception as e:
        print(f"[ERROR] Gagal extract gambar via Tavily: {e}")
        for article in articles:
            article.setdefault("images", [])
        return articles