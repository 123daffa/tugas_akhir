import io
import requests
from PIL import Image
from app.core.constants import MIN_IMAGE_DIMENSION
from app.models.clip_model import clip_handler


def _load_image(image_source: str, timeout: int = 5) -> Image.Image | None:
    """
    Download gambar artikel (URL asli hasil ekstraksi Tavily) untuk CLIP.
    langsung masuk sebagai PIL.Image (lihat compute_image_similarity).
    """
    try:
        url_lower = image_source.lower().split("?")[0]

        # Skip aset non-konten: logo, placeholder, ikon UI, badge app, banner iklan
        skip_patterns = [
            ".svg", ".gif", "logo", "kontent-kosong", "konten-kosong", "placeholder",
            "favicon", "googleplay", "appstore", "playstore", "icon-light-mode",
            "icon-night-mode", "728x90", "300x250", "160x600",  # ukuran standar banner iklan
        ]
        if any(pattern in url_lower for pattern in skip_patterns):
            return None

        headers = {"User-Agent": "Mozilla/5.0 (compatible; FactCheckBot/1.0)"}
        resp = requests.get(image_source, headers=headers, timeout=timeout)
        resp.raise_for_status()
        img = Image.open(io.BytesIO(resp.content)).convert("RGB")
    
        if img.width < MIN_IMAGE_DIMENSION or img.height < MIN_IMAGE_DIMENSION:
            print(f"[WARNING] Gambar terlalu kecil ({img.width}x{img.height}), dilewati: {image_source[:80]}")
            return None

        return img
    except Exception as e:
        print(f"[WARNING] Gagal muat gambar untuk CLIP ({image_source[:80]}...): {e}")
        return None


def compute_image_similarity(user_image, reference_image_urls: list) -> float:
    """
    Similarity TERTINGGI antara gambar user vs gambar-gambar referensi.
    Return cosine similarity mentah (bukan skala 0-1 intuitif).
    """

    if user_image is None:
        return 0.0

    best_score = None
    for ref_url in reference_image_urls[:5]:
        ref_img = _load_image(ref_url)
        if ref_img is None:
            continue
        score = clip_handler.get_image_similarity(user_image, ref_img)
        print(f"[INFO]   → similarity vs {ref_url}: {score:.4f}")
        if best_score is None or score > best_score:
            best_score = score

    return round(best_score, 4) if best_score is not None else 0.0


def encode_frames(frames: list):
    """Precompute embedding untuk semua frame SEKALI SAJA, dipakai ulang
    untuk perbandingan terhadap gambar referensi artikel manapun."""
    return [clip_handler.get_image_embedding(f) for f in frames]


def compute_video_similarity_from_embeddings(frame_embeddings: list, reference_image_urls: list) -> float:
    """Sama seperti compute_video_similarity, tapi menerima embedding frame
    yang SUDAH dihitung sebelumnya (bukan raw frame), supaya tidak di-encode
    ulang untuk tiap artikel."""
    reference_images = []
    for ref_url in reference_image_urls[:5]:
        ref_img = _load_image(ref_url)
        if ref_img is not None:
            reference_images.append(ref_img)

    if not reference_images or not frame_embeddings:
        return 0.0

    ref_embeddings = []
    for r in reference_images:
        try:
            ref_embeddings.append(clip_handler.get_image_embedding(r))
        except Exception as e:
            print(f"[WARNING] Gagal encode gambar referensi, dilewati: {e}")

    if not ref_embeddings:
        return 0.0

    best_score = None
    for f_emb in frame_embeddings:
        for r_emb in ref_embeddings:
            score = (f_emb @ r_emb.T).item()
            if best_score is None or score > best_score:
                best_score = score

    return round(best_score, 4) if best_score is not None else 0.0