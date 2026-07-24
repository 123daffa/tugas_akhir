from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Config
from app.routes.text_routes import text_bp
from app.routes.image_routes import image_bp
# from app.routes.video_routes import video_bp
from extensions import db, jwt, cors

def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config)

    # Konfigurasi ukuran maksimum upload
    # 50MB untuk video, 10MB untuk gambar
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB

    # CORS untuk Vue.js frontend
    CORS(app, origins=["http://localhost:5173"])
    # CORS(app, origins=["216.198.79.1"])

    # Register semua blueprint dengan prefix /api
    app.register_blueprint(text_bp, url_prefix="/api")
    app.register_blueprint(image_bp, url_prefix="/api")
    # app.register_blueprint(video_bp, url_prefix="/api")

    # Health check endpoint
    @app.get("/")
    def health_check():
        return jsonify({"status": "running"})

    # Handler error ukuran file terlalu besar
    @app.errorhandler(413)
    def file_too_large(e):
        return jsonify({"detail": "Ukuran file terlalu besar (maksimum 50MB)"}), 413

    return app