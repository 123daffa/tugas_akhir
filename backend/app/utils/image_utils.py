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


def compress_image_to_data_uri(image_bytes: bytes, compress: bool = True) -> str:
    """
    Ubah bytes gambar (upload user) jadi base64 data URI, dengan opsi
    kompresi dulu. Dipakai di image_routes.py sebelum gambar masuk pipeline.
    """
    if compress:
        image_bytes = _compress_image_bytes(image_bytes)
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"