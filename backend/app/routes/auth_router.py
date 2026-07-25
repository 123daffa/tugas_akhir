from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    result = AuthService.register(data.get('fullName'), data.get('email'), data.get('password'))
    return jsonify(result), 201


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    result = AuthService.login(data.get('email'), data.get('password'))
    return jsonify(result), 200