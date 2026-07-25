from extensions import db
from app.models import User


class UserRepository:
    """Semua query ke tabel users ada di sini. Service dan route TIDAK boleh
    memanggil User.query langsung — panggil method di kelas ini."""

    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def email_taken(email, exclude_id=None):
        query = User.query.filter(User.email == email)
        if exclude_id:
            query = query.filter(User.id != exclude_id)
        return query.first() is not None

    @staticmethod
    def search(search_term, page, per_page):
        query = User.query
        if search_term:
            query = query.filter(db.or_(
                User.full_name.ilike(f'%{search_term}%'),
                User.email.ilike(f'%{search_term}%')
            ))
        return query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def count():
        return User.query.count()

    @staticmethod
    def create(full_name, email, password):
        user = User(full_name=full_name, email=email, role='user')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def save(user):
        db.session.commit()
        return user

    @staticmethod
    def delete(user):
        db.session.delete(user)
        db.session.commit()