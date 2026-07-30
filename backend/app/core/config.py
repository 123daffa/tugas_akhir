import os
import torch
from dotenv import load_dotenv

load_dotenv()  # baca file .env

class Settings:
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"
    TRANSLATOR_MODEL_NAME = "Helsinki-NLP/opus-mt-id-en"
    GROQ_VISION_MODEL="qwen/qwen3.6-27b"

    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

settings = Settings()

print(f"[INFO] Menggunakan device: {settings.DEVICE}")