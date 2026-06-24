# test_summarizer_manual.py (di folder backend/)
from app.services.summarizer_service import summarize_caption

text = "Wakil Kepala Badan Gizi Nasional (BGN) Agustina Arumsari merespons 41 nama diduga terlibat korupsi tata kelola Makan Bergizi Gratis (MBG) yang dibeberkan mantan Waka BGN Sony Sanjaya. Dia mempersilakan Kejaksaan Agung (Kejagung) menyelidikinya."

query = summarize_caption(text, top_k=10)
print(f"Query hasil: {query}")