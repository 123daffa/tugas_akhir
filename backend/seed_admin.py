from app import create_app
from extensions import db
from app.models.user import User

app = create_app()

with app.app_context():
    admin = User.query.filter_by(email="admin@gmail.com").first()

    if not admin:
        admin = User(
            full_name="Administrator",
            email="admin@gmail.com",
            role="admin"
        )
        admin.set_password("Admin12345")
        db.session.add(admin)
        db.session.commit()
        print("Admin berhasil dibuat.")
    else:
        print("Admin sudah ada.")