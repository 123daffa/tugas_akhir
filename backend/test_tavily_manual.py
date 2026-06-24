from tavily import TavilyClient
from app.services.summarizer_service import summarize_caption
from app.core.config import settings

text = "Wakil Kepala Badan Gizi Nasional (BGN) Agustina Arumsari merespons 41 nama diduga terlibat korupsi tata kelola Makan Bergizi Gratis (MBG) yang dibeberkan mantan Waka BGN Sony Sanjaya. Dia mempersilakan Kejaksaan Agung (Kejagung) menyelidikinya."

query = summarize_caption(text, top_k=10)
print(f"Query hasil: {query}")

client = TavilyClient(settings.TAVILY_API_KEY)
response = client.search(
    query=query,
    topic="news",
    search_depth="advanced",
    max_results=5,
    include_usage=True
)
print(response)