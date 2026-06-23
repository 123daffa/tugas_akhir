import torch

class Settings:
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"

settings = Settings()

print(f"[INFO] Menggunakan device: {settings.DEVICE}")