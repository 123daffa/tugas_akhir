class ServiceError(Exception):
    """Exception dasar untuk semua error yang berasal dari service layer.
    Ditangkap secara global di app/__init__.py, jadi routes tidak perlu try/except lagi."""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundError(ServiceError):
    def __init__(self, message='Data tidak ditemukan.'):
        super().__init__(message, 404)


class ForbiddenError(ServiceError):
    def __init__(self, message='Anda tidak memiliki akses.'):
        super().__init__(message, 403)


class ConflictError(ServiceError):
    def __init__(self, message='Data sudah ada.'):
        super().__init__(message, 409)


class UnauthorizedError(ServiceError):
    def __init__(self, message='Tidak diizinkan.'):
        super().__init__(message, 401)