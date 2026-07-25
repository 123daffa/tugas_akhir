from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.pipelines.text_pipeline import run_text_pipeline
from app.schemas.text_schema import TextCheckResponse
from app.schemas.common_schema import ErrorResponse
from app.services.history_service import HistoryService

text_bp = Blueprint("text", __name__)

@text_bp.route("/check/text", methods=["POST"])
@jwt_required()
def check_text():
    data = request.get_json()

    # Validasi input
    if not data or "text" not in data:
        return jsonify(
            ErrorResponse(detail="Field 'text' wajib diisi").to_dict()
        ), 400

    if len(data["text"]) < 10:
        return jsonify(
            ErrorResponse(detail="Teks minimal 10 karakter").to_dict()
        ), 400

    try:
        result = run_text_pipeline(data["text"])
        response = TextCheckResponse(**result)
        user_id = get_jwt_identity()

        try:
            HistoryService.save_check_result(
                user_id, mode="text", result=result, input_text=data["text"]
            )
        except Exception as e:
            print(f"[WARNING] gagal simpan history (text): {e}")
                
        return jsonify(response.to_dict()), 200

    except Exception as e:
        print(f"[ERROR] text pipeline: {e}")
        return jsonify(ErrorResponse(detail=str(e)).to_dict()), 500