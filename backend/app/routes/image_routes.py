from flask import Blueprint, request, jsonify
from app.pipelines.image_pipeline import run_image_pipeline
from app.schemas.image_schema import ImageCheckResponse
from app.schemas.common_schema import ErrorResponse

image_bp = Blueprint("image", __name__)

@image_bp.route("/check/image", methods=["POST"])
def check_image():
    # Validasi file dan caption
    if "image" not in request.files:
        return jsonify(
            ErrorResponse(detail="File 'image' wajib disertakan").to_dict()
        ), 400

    if "caption" not in request.form:
        return jsonify(
            ErrorResponse(detail="Field 'caption' wajib diisi").to_dict()
        ), 400

    image_file = request.files["image"]
    caption = request.form["caption"]

    # Validasi ekstensi file
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    filename = image_file.filename.lower()
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        return jsonify(
            ErrorResponse(detail="Format gambar tidak didukung. Gunakan JPG, PNG, atau WEBP").to_dict()
        ), 400

    try:
        image_bytes = image_file.read()
        result = run_image_pipeline(image_bytes, caption)
        response = ImageCheckResponse(**result)
        return jsonify(response.to_dict()), 200

    except Exception as e:
        print(f"[ERROR] image pipeline: {e}")
        return jsonify(ErrorResponse(detail=str(e)).to_dict()), 500