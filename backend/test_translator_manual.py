from app.models.translator_model import translator_handler

# Pakai teks apapun yang ada di komputer untuk testing
text = "Venezuela earthquakes live: Tremors of 7.5, 7.2 kill 32, injure hundreds"
# Test 1: terjemahan yang sesuai
translated_text = translator_handler.translate(text)
print(f"Terjemahan: {translated_text}")