from tavily import TavilyClient
from app.services.summarizer_service import summarize_caption
from app.core.config import settings


client = TavilyClient(settings.TAVILY_API_KEY)
response = client.search(
    query="",
    topic="news",
    search_depth="advanced",
    max_results=5,
    include_usage=True
)
print(response)