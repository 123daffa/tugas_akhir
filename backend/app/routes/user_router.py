from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService

user_bp = Blueprint('user', __name__)


@user_bp.route('/user/me', methods=['GET'])
@jwt_required()
def get_me():
    return jsonify(UserService.get_me(get_jwt_identity())), 200


@user_bp.route('/user/me', methods=['PUT'])
@jwt_required()
def update_me():
    data = request.get_json(silent=True) or {}
    result = UserService.update_me(get_jwt_identity(), data.get('fullName'), data.get('email'))
    return jsonify(result), 200


@user_bp.route('/user/me/password', methods=['PUT'])
@jwt_required()
def change_password():
    data = request.get_json(silent=True) or {}
    UserService.change_password(get_jwt_identity(), data.get('currentPassword'), data.get('newPassword'))
    return jsonify({'message': 'Password berhasil diubah.'}), 200