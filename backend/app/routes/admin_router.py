from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.admin_service import AdminService
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/users', methods=['GET'])
@jwt_required()
@admin_required
def list_users():
    result = AdminService.list_users(
        request.args.get('q', ''),
        request.args.get('page', 1, type=int),
        request.args.get('per_page', 10, type=int)
    )
    return jsonify(result), 200


@admin_bp.route('/admin/users', methods=['POST'])
@jwt_required()
@admin_required
def create_user():
    data = request.get_json(silent=True) or {}
    return jsonify(AdminService.create_user(data)), 201


@admin_bp.route('/admin/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user_detail(user_id):
    return jsonify(AdminService.get_user_detail(user_id)), 200


@admin_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    data = request.get_json(silent=True) or {}
    return jsonify(AdminService.update_user(user_id, data)), 200


@admin_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    AdminService.delete_user(get_jwt_identity(), user_id)
    return jsonify({'message': 'User berhasil dihapus.'}), 200


@admin_bp.route('/admin/content', methods=['GET'])
@jwt_required()
@admin_required
def list_content():
    result = AdminService.list_content(
        request.args.get('category'),
        request.args.get('q', ''),
        request.args.get('page', 1, type=int),
        request.args.get('per_page', 10, type=int)
    )
    return jsonify(result), 200


@admin_bp.route('/admin/content/<int:content_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_content_detail(content_id):
    return jsonify(AdminService.get_content_detail(content_id)), 200


@admin_bp.route('/admin/content/<int:content_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_content(content_id):
    AdminService.delete_content(content_id)
    return jsonify({'message': 'Konten berhasil dihapus.'}), 200


@admin_bp.route('/admin/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_stats():
    return jsonify(AdminService.get_stats()), 200