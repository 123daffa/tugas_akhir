from tavily import TavilyClient
from app.core.config import settings


def get_search_client():
    return TavilyClient(settings.TAVILY_API_KEY)

def search_related_news(query: str):
    client = get_search_client()
    response = client.search(
        query=query,
        topic="news",
        search_depth="advanced",
        max_results=5,
        include_usage=True,
        include_domains=["detik.com", "kompas.com", "cnnindonesia.com", "tribunnews.com", "liputan6.com"]
)
    return response