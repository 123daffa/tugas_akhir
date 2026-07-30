from tavily import TavilyClient
from app.core.constants import TAVILY_MAX_RESULTS, TAVILY_SEARCH_DEPTH, TAVILY_TOPIC
from app.core.config import settings

tavily_client = TavilyClient(settings.TAVILY_API_KEY)

def search_related_news_gambar(query: str, include_images: bool = False) -> dict:
    
    try: 
        client = tavily_client
        response = client.search(
            query=query,
            topic=TAVILY_TOPIC,
            search_depth=TAVILY_SEARCH_DEPTH,
            max_results=TAVILY_MAX_RESULTS,
            include_images=include_images    
        )

        results = response.get("results", [])

        print(f"[INFO] Tavily menemukan {len(results)} artikel untuk query: '{query}'")
        for article in results:
            gambar_artikel = article.get("images", [])
            print(f"  - {article.get('title')} ({article.get('url')}) | Score: {article.get('score')} | Gambar: {len(gambar_artikel)}")

        return {
            "articles": results,  # tiap artikel sekarang bisa punya key 'images' sendiri
        }

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat mencari berita terkait: {e}")
        return {
            "articles": [],
        }

def get_first_image(article: dict) -> str | None:
    """Ambil gambar pertama dari sebuah artikel, kalau ada."""
    images = article.get("images", [])
    return images[0] if images else None