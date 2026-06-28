import torch
from transformers import AutoTokenizer, AutoModel
from app.core.config import settings

class IndoBERTHandler:
    def __init__(self):
        self.device = settings.DEVICE    
        self.tokenizer = AutoTokenizer.from_pretrained(settings.INDOBERT_MODEL_NAME)
        self.model = AutoModel.from_pretrained(settings.INDOBERT_MODEL_NAME).to(self.device)
        self.model.eval()
        
        print(f"[INFO] IndoBERT model loaded on {self.device}")

    def get_embedding(self, text: str) -> torch.Tensor:
        """Menghasilkan embedding untuk satu teks (kata/frasa/kalimat)."""
        inputs = self.tokenizer(
            text,
            return_tensors="pt", # mengembalikan hasil tokenisasi dalam format tensor PyTorch
            truncation=True, # memotong teks yang terlalu panjang agar sesuai dengan panjang maksimum model
            padding=True, # menambahkan padding agar semua input memiliki panjang yang sama
            max_length=128
        ).to(self.device)

        with torch.no_grad(): # menonaktifkan perhitungan gradient selama proses inferensi, sehingga menghemat memori dan mempercepat proses.
            outputs = self.model(**inputs) 

        # Mean pooling dari semua token, jadi 1 vektor representatif
        embedding = outputs.last_hidden_state.mean(dim=1)
        return embedding.squeeze(0)  # shape: (768,)


# Singleton instance
indobert_handler = IndoBERTHandler()