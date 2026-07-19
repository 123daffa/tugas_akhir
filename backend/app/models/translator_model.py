import torch
from transformers import MarianMTModel, MarianTokenizer
from app.core.config import settings

class TranslatorHandler:
    def __init__(self):
        self.device = settings.DEVICE    
        self.tokenizer = MarianTokenizer.from_pretrained(settings.TRANSLATOR_MODEL_NAME)
        self.model = MarianMTModel.from_pretrained(settings.TRANSLATOR_MODEL_NAME).to(self.device)
        self.model.eval()
        
        print(f"[INFO] Translator model loaded on {self.device}")

    def translate(self, text: str) -> str:
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        ).to(self.device)

        translated = self.model.generate(**inputs)
        result = self.tokenizer.decode(translated[0], skip_special_tokens=True)
        print(f"[INFO] Hasil translate indo => eng: '{result}'")
        return result
    
# Singleton instance
translator_handler = TranslatorHandler()
    
