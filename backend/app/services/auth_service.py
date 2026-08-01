from flask_jwt_extended import create_access_token
from app.repositories.user_repository import UserRepository
from app.utils.errors import ServiceError, ConflictError, UnauthorizedError


class AuthService:
    @staticmethod
    def register(full_name, email, password):
        full_name = (full_name or '').strip()
        email = (email or '').strip().lower()

        if not full_name or not email or not password:
            raise ServiceError('Nama, email, dan password wajib diisi.')
        if len(password) < 8:
            raise ServiceError('Password minimal 8 karakter.')
        if UserRepository.find_by_email(email):
            raise ConflictError('Email sudah terdaftar.')

        user = UserRepository.create(full_name, email, password)
        return {'user': user.to_dict()}

    @staticmethod
    def login(email, password):
        email = (email or '').strip().lower()
        user = UserRepository.find_by_email(email)
        if not user or not user.check_password(password):
            raise UnauthorizedError('Email atau password salah.')
        token = create_access_token(identity=str(user.id))
        return {'token': token, 'user': user.to_dict()}