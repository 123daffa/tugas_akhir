import base64

from groq import Groq

from app.core.config import settings


class GroqVisionHandler:

    def __init__(self):
        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_VISION_MODEL

        print(f"[INFO] Groq Vision loaded: {self.model}")


    def generate_caption(self, image_path: str) -> str:
        """
        Mengubah gambar menjadi caption singkat
        menggunakan Groq Vision.
        """

        # membaca gambar
        with open(image_path, "rb") as image_file:
            image_base64 = base64.b64encode(
                image_file.read()
            ).decode("utf-8")


        response = self.client.chat.completions.create(
            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": [

                        {
                            "type": "text",
                            "text": """
Generate a concise image caption.

Describe only:
- main subject
- important objects
- visible action
- relevant context

Rules:
- Return only one sentence.
- Do not explain.
- Do not mention uncertainty.
- Do not add extra information.
"""
                        },

                        {
                            "type": "image_url",
                            "image_url": {
                                "url":
                                f"data:image/jpeg;base64,{image_base64}"
                            }
                        }

                    ]
                }
            ],

            temperature=0.2,
            max_tokens=100
        )


        caption = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )


        print(f"[INFO] Generated Caption: {caption}")


        return caption



# Singleton instance
groq_vision_handler = GroqVisionHandler()