import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug ikut environment: True hanya kalau FLASK_ENV=development (di .env)
    # host 0.0.0.0 supaya bisa diakses dari luar localhost (HP di jaringan sama, Docker, dll)
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=os.getenv("FLASK_ENV", "development") == "development"
    )