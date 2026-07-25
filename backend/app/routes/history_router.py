from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.history_service import HistoryService

history_bp = Blueprint('history', __name__)


@history_bp.route('/history', methods=['GET'])
@jwt_required()
def list_history():
    result = HistoryService.list_for_user(
        get_jwt_identity(),
        category=request.args.get('category'),
        search_term=request.args.get('q', ''),
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', 8, type=int)
    )
    return jsonify(result), 200


@history_bp.route('/history/<int:history_id>', methods=['GET'])
@jwt_required()
def get_history_detail(history_id):
    result = HistoryService.get_detail(get_jwt_identity(), history_id)
    return jsonify(result), 200