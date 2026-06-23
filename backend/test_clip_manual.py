# test_clip_manual.py (taruh di folder backend/, sejajar dengan app/)
from app.models.clip_model import clip_handler
from PIL import Image

# Pakai gambar apapun yang ada di komputer untuk testing
image = Image.open("contoh_gambar.jpg").convert("RGB")

# Test 1: caption yang sesuai
score_sesuai = clip_handler.get_similarity(image, "picture a brown horse running in a field")
print(f"Caption sesuai: {score_sesuai}")

# Test 2: caption yang tidak sesuai
score_tidak_sesuai = clip_handler.get_similarity(image, "picture a car driving on a busy street")
print(f"Caption tidak sesuai: {score_tidak_sesuai}")