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

    def get_similarity(self, image, text: str) -> float:
        inputs = self.processor(
            text=[text],
            images=image,
            return_tensors="pt",
        ).to(self.device) 

        with torch.no_grad(): # menonaktifkan perhitungan gradient selama proses inferensi.
            outputs = self.model(**inputs) # menghasilkan embedding untuk gambar dan teks menggunakan model CLIP.

        image_embeds = outputs.image_embeds
        text_embeds = outputs.text_embeds

        image_embeds = image_embeds / image_embeds.norm(dim=-1, keepdim=True)
        text_embeds = text_embeds / text_embeds.norm(dim=-1, keepdim=True)

        similarity = (image_embeds @ text_embeds.T).item() # menghitung dot product antara embedding gambar dan teks

        # print("Image shape:", image_embeds.shape)
        # print("Text shape:", text_embeds.shape)

        # dot_product = image_embeds @ text_embeds.T
        # print("Dot Product:", dot_product)

        # similarity = dot_product.item()
        # print("Similarity:", similarity)

        print(f"[INFO] Similarity antara caption dan content: '{similarity}'")

        return similarity


# Singleton instance — dibuat sekali saat startup, dipakai berulang
clip_handler = CLIPHandler()