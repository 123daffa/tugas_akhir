import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config_by_name
from extensions import db, jwt

from app.utils.errors import ServiceError
from app.routes.text_routes import text_bp
from app.routes.image_routes import image_bp
from app.routes.video_routes import video_bp

from app.routes.auth_router import auth_bp
from app.routes.user_router import user_bp
from app.routes.history_router import history_bp
from app.routes.admin_router import admin_bp


def create_app(env_name=None):
    app = Flask(__name__)
    env_name = env_name or os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_by_name[env_name])

    # Konfigurasi ukuran maksimum upload
    # 50MB untuk video, 10MB untuk gambar
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB

    # CORS untuk Vue.js frontend
    CORS(app, origins=["http://localhost:5173"])
    # CORS(app, origins=["216.198.79.1"])

    db.init_app(app)
    jwt.init_app(app)

    # Register semua blueprint dengan prefix /api
    app.register_blueprint(text_bp, url_prefix="/api")
    app.register_blueprint(image_bp, url_prefix="/api")
    app.register_blueprint(video_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")

    # Health check endpoint
    @app.get("/")
    def health_check():
        return jsonify({"status": "running"})

    # Handler error ukuran file terlalu besar
    @app.errorhandler(413)
    def file_too_large(e):
        return jsonify({"detail": "Ukuran file terlalu besar (maksimum 50MB)"}), 413

    @app.errorhandler(ServiceError)
    def handle_service_error(e):
        return jsonify({"message": e.message}), e.status_code

    with app.app_context():
        if app.config.get("DEBUG"):
            db.create_all()
    return app