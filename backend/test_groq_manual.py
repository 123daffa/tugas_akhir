# test_groq_summarize.py (di folder backend/)
from app.services.groq_service import summarize_tavily_results

# Simulasi hasil Tavily (tanpa perlu hit Tavily API)
mock_tavily_results = [
    {
        "title": "Zelenskyy Masih Hidup, Bantah Kabar Kematian",
        "content": "Presiden Ukraina Volodymyr Zelenskyy membantah kabar yang menyebutkan dirinya tewas dalam serangan udara Rusia. Zelenskyy muncul dalam video langsung dan menegaskan kondisinya baik-baik saja.",
        "score": 0.91
    },
    {
        "title": "Rusia Lancarkan Serangan Udara ke Kyiv",
        "content": "Militer Rusia melancarkan serangkaian serangan udara ke wilayah Kyiv dan sekitarnya. Pihak berwenang Ukraina melaporkan beberapa infrastruktur sipil terdampak namun tidak ada korban jiwa dari pejabat tinggi.",
        "score": 0.85
    },
    {
        "title": "NATO Pantau Situasi Ukraina Pasca Serangan",
        "content": "NATO menyatakan terus memantau perkembangan situasi di Ukraina setelah serangkaian serangan Rusia. Juru bicara NATO menegaskan tidak ada indikasi kematian pemimpin Ukraina.",
        "score": 0.78
    }
]

original_text = """Laporan menyebutkan serangan udara Rusia menargetkan lokasi aman 
di Ukraina, yang diduga membunuh Presiden Volodymyr Zelenskyy."""

print("=" * 60)
print("TEST GROQ SUMMARIZE TAVILY RESULTS")
print("=" * 60)
print(f"\nKlaim yang diperiksa:\n{original_text.strip()}")
print(f"\nJumlah artikel mock: {len(mock_tavily_results)}")
print("\nMemproses...")

result = summarize_tavily_results(mock_tavily_results, original_text)

print("\n[HASIL SUMMARIZE]")
print("-" * 40)
print(result)
print("-" * 40)