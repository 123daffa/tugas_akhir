import torch
from transformers import AutoTokenizer, AutoModel
from app.core.config import settings

class IndoBERTHandler:
    def __init__(self):
        self.device = settings.DEVICE
        self.model_name = "indobenchmark/indobert-base-p1"
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name).to(self.device)
        self.model.eval()
        
        print(f"[INFO] IndoBERT model loaded on {self.device}")

    def get_embedding(self, text: str) -> torch.Tensor:
        """Menghasilkan embedding untuk satu teks (kata/frasa/kalimat)."""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        # Mean pooling dari semua token, jadi 1 vektor representatif
        embedding = outputs.last_hidden_state.mean(dim=1)
        return embedding.squeeze(0)  # shape: (768,)


# Singleton instance
indobert_handler = IndoBERTHandler()