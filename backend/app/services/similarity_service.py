from app.models.clip_model import clip_handler
from PIL import Image
import io

def calculate_image_text_similarity(image_bytes: bytes, caption: str) -> float:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    score = clip_handler.get_similarity(image, caption)
    return score