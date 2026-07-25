from app.repositories.user_repository import UserRepository
from app.utils.errors import NotFoundError, ConflictError, ServiceError, UnauthorizedError


class UserService:
    @staticmethod
    def get_me(user_id):
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise NotFoundError('User tidak ditemukan.')
        return user.to_dict()

    @staticmethod
    def update_me(user_id, full_name, email):
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise NotFoundError('User tidak ditemukan.')

        full_name = (full_name or '').strip()
        email = (email or '').strip().lower()
        if not full_name or not email:
            raise ServiceError('Nama dan email tidak boleh kosong.')
        if UserRepository.email_taken(email, exclude_id=user.id):
            raise ConflictError('Email sudah digunakan akun lain.')

        user.full_name = full_name
        user.email = email
        UserRepository.save(user)
        return user.to_dict()

    @staticmethod
    def change_password(user_id, current_password, new_password):
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise NotFoundError('User tidak ditemukan.')
        if not user.check_password(current_password or ''):
            raise UnauthorizedError('Password lama tidak sesuai.')
        if len(new_password or '') < 8:
            raise ServiceError('Password baru minimal 8 karakter.')

        user.set_password(new_password)
        UserRepository.save(user)