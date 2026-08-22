import base64
from io import BytesIO
from PIL import Image
from app.core.constants import MAX_DIMENSION, JPEG_QUALITY

def _compress_image_bytes(image_bytes: bytes) -> bytes:
    """
    Resize + kompres gambar. CLIP maupun proses lain tidak butuh resolusi
    tinggi untuk membandingkan kemiripan gambar.
    """
    try:
        img = Image.open(BytesIO(image_bytes))
        img = img.convert("RGB")  # buang alpha channel, standarkan ke JPEG
        img.thumbnail((MAX_DIMENSION, MAX_DIMENSION))
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=JPEG_QUALITY)
        return buffer.getvalue()
    except Exception as e:
        print(f"[WARNING] Gagal kompres gambar, pakai versi asli: {e}")
        return image_bytes
