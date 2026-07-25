import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()  # baca file .env


class Config:
    """Config dasar, dipakai semua environment."""
    SECRET_KEY = os.getenv("SECRET_KEY", "ganti-ini-di-.env")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "ganti-ini-juga-di-.env")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    SUPABASE_STORAGE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "detection-media")

    SQLALCHEMY_DATABASE_URI = os.getenv("SUPABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    # pakai SQLite in-memory saat testing supaya tidak menyentuh DB Supabase asli
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}