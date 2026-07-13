from tavily import TavilyClient
from app.core.constants import TAVILY_MAX_RESULTS, TAVILY_SEARCH_DEPTH, TAVILY_TOPIC, INCLUDE_DOMAINS
from app.core.config import settings


tavily_client = TavilyClient(settings.TAVILY_API_KEY)

def search_related_news(query: str) -> list:

    try: 
        client = tavily_client
        response = client.search(
            query=query,
            topic=TAVILY_TOPIC,
            search_depth=TAVILY_SEARCH_DEPTH,
            max_results=TAVILY_MAX_RESULTS,
            include_usage=True,
            include_domains=INCLUDE_DOMAINS
        )
        
        results = response.get("results", [])
        print(f"[INFO] Tavily menemukan {len(results)} artikel untuk query: '{query}'")
        for article in results:
            print(f"  - {article.get('title')} ({article.get('url')}) | Score: {article.get('score')}")
        return results

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat mencari berita terkait: {e}")
        return []