import uuid
from io import BytesIO
from flask import current_app
from supabase import create_client


def _get_client():
    return create_client(
        current_app.config["SUPABASE_URL"],
        current_app.config["SUPABASE_SERVICE_ROLE_KEY"]
    )


def upload_bytes(file_bytes: bytes, extension: str, folder: str = "thumbnails") -> str:
    """Upload bytes mentah ke Supabase Storage, kembalikan public URL-nya.
    `extension` tanpa titik, misal 'jpg', 'png', 'webp'."""
    client = _get_client()
    bucket = current_app.config["SUPABASE_STORAGE_BUCKET"]
    extension = extension.lstrip(".").lower()
    filename = f"{folder}/{uuid.uuid4().hex}.{extension}"

    client.storage.from_(bucket).upload(
        filename,
        file_bytes,
        {"content-type": f"image/{extension}"}
    )
    return client.storage.from_(bucket).get_public_url(filename)


def upload_pil_image(pil_image, folder: str = "thumbnails") -> str:
    """Upload PIL.Image (dipakai untuk frame pertama video) ke Supabase Storage
    sebagai JPEG, kembalikan public URL-nya."""
    buffer = BytesIO()
    pil_image.convert("RGB").save(buffer, format="JPEG", quality=85)
    return upload_bytes(buffer.getvalue(), "jpg", folder)