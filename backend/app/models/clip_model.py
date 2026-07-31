import torch
from transformers import CLIPModel, CLIPProcessor
from app.core.config import settings

# clip processor menyiapkan data (gambar dan teks) agar sesuai dengan format yang diharapkan oleh model CLIP.
# clip model digunakan untuk menghasilkan embedding (representasi vektor) dari gambar dan teks, yang kemudian dapat 
# digunakan untuk menghitung kesamaan antara keduanya.

class CLIPHandler:
    def __init__(self):
        self.device = settings.DEVICE
        self.model = CLIPModel.from_pretrained(settings.CLIP_MODEL_NAME).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(settings.CLIP_MODEL_NAME)
        self.model.eval()  # mode evaluasi, bukan training

        print(f"[INFO] CLIP model loaded on {self.device}")

    def get_image_embedding(self, image):
        """Ambil embedding gambar saja (dinormalisasi)."""
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)

        with torch.no_grad():
            image_embeds = self.model.get_image_features(**inputs)

        image_embeds = image_embeds / image_embeds.norm(dim=-1, keepdim=True)
        return image_embeds

    def get_image_similarity(self, image1, image2) -> float:
        """Similarity antara DUA gambar (image-image)."""
        embed1 = self.get_image_embedding(image1)
        embed2 = self.get_image_embedding(image2)

        similarity = (embed1 @ embed2.T).item()

        print(f"[INFO] Similarity antar gambar: '{similarity}'")

        return similarity


# Singleton instance — dibuat sekali saat startup, dipakai berulang
clip_handler = CLIPHandler()