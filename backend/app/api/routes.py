from fastapi import APIRouter, UploadFile, Form
from app.services.similarity_service import calculate_image_text_similarity

router = APIRouter()

@router.post("/check-similarity")
async def check_similarity(
    image: UploadFile,
    caption: str = Form(...)
):
    image_bytes = await image.read()
    score = calculate_image_text_similarity(image_bytes, caption)

    return {
        "similarity_score": round(score, 4)
    }