from flask import Blueprint, request, jsonify
from app.pipelines.video_pipeline import run_video_pipeline
from app.schemas.video_schema import VideoCheckResponse
from app.schemas.common_schema import ErrorResponse

video_bp = Blueprint("video", __name__)

@video_bp.route("/check/video", methods=["POST"])
def check_video():
    if "video" not in request.files:
        return jsonify(
            ErrorResponse(detail="File 'video' wajib disertakan").to_dict()
        ), 400

    if "caption" not in request.form:
        return jsonify(
            ErrorResponse(detail="Field 'caption' wajib diisi").to_dict()
        ), 400

    video_file = request.files["video"]
    caption = request.form["caption"]

    allowed_extensions = {".mp4", ".mov", ".avi"}
    filename = video_file.filename.lower()
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        return jsonify(
            ErrorResponse(detail="Format video tidak didukung. Gunakan MP4, MOV, atau AVI").to_dict()
        ), 400

    try:
        video_bytes = video_file.read()
        result = run_video_pipeline(video_bytes, caption)
        response = VideoCheckResponse(**result)
        return jsonify(response.to_dict()), 200

    except Exception as e:
        print(f"[ERROR] video pipeline: {e}")
        return jsonify(ErrorResponse(detail=str(e)).to_dict()), 500