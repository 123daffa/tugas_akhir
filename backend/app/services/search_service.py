from tavily import TavilyClient
from backend.app.core.constants import TAVILY_MAX_RESULTS, TAVILY_SEARCH_DEPTH, TAVILY_TOPIC, INCLUDE_DOMAINS
from app.core.config import settings


def get_search_client():
    return TavilyClient(settings.TAVILY_API_KEY)

def search_related_news(query: str):
    client = get_search_client()
    response = client.search(
        query=query,
        topic=TAVILY_TOPIC,
        search_depth=TAVILY_SEARCH_DEPTH,
        max_results=TAVILY_MAX_RESULTS,
        include_usage=True,
        include_domains=INCLUDE_DOMAINS
    )
    return response