from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = User.query.get(get_jwt_identity())
        if not user or not user.is_admin:
            return jsonify({'message': 'Akses ditolak. Fitur ini khusus admin.'}), 403
        return fn(*args, **kwargs)
    return wrapper