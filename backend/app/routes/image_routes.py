import base64
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.pipelines.image_pipeline import run_image_pipeline
from app.schemas.image_schema import ImageCheckResponse
from app.schemas.common_schema import ErrorResponse
from app.services.history_service import HistoryService
from app.services.storage_service import upload_bytes
from app.services.groq_vision_service import compress_image_to_data_uri

image_bp = Blueprint("image", __name__)


@image_bp.route("/check/image", methods=["POST"])
@jwt_required()
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
        extension = filename.rsplit(".", 1)[-1]

        # Kompres + encode ke base64 data URI sebelum masuk pipeline.
        # Diperlukan karena Groq Vision butuh data URI/URL (bukan bytes mentah),
        # dan kompresi mengurangi ukuran token supaya tidak kena rate limit TPM
        # (gambar ini dikirim ulang ke Groq untuk tiap artikel yang dicek).
        image_data_uri = compress_image_to_data_uri(image_bytes)

        result = run_image_pipeline(image_data_uri, caption)
        response = ImageCheckResponse(**result)

        user_id = get_jwt_identity()

        image_path = None
        try:
            # upload_bytes tetap pakai bytes asli (bukan versi kompresi),
            # supaya file yang disimpan ke storage tetap kualitas penuh
            image_path = upload_bytes(image_bytes, extension, folder="images")
        except Exception as e:
            print(f"[WARNING] gagal upload gambar ke storage: {e}")

        try:
            HistoryService.save_check_result(
                user_id, mode="image", result=result, caption=caption, image_path=image_path
            )
        except Exception as e:
            print(f"[WARNING] gagal simpan history (image): {e}")

        return jsonify(response.to_dict()), 200

    except Exception as e:
        print(f"[ERROR] image pipeline: {e}")
        return jsonify(ErrorResponse(detail=str(e)).to_dict()), 500