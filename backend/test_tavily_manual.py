from tavily import TavilyClient
from app.core.config import settings

text = "Prabowo Tanya Guru Besar: Kenapa 81 Tahun RI Tak Bisa Bikin Mobil Sendiri?"

client = TavilyClient(settings.TAVILY_API_KEY)
response = client.search(
    query=text,
    topic="news",
    search_depth="advanced",
    max_results=5,
    include_usage=True,
    include_domains=["detik.com", "kompas.com", "cnnindonesia.com", "tribunnews.com", "liputan6.com"]
)

result = response.get("results", [])
print (f"[INFO] Tavily menemukan {len(result)} artikel untuk query: '{text}'")
print(result)


