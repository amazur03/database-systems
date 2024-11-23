from flask import Blueprint, jsonify, request
from services.warehouse_move_service import (
    get_all_warehouse_moves,
    get_warehouse_move_by_id,
    add_warehouse_move,
    update_warehouse_move,
    delete_warehouse_move
)

warehouse_move_blueprint = Blueprint('warehouse_moves', __name__)

@warehouse_move_blueprint.route('/warehouse_moves', methods=['GET'])
def list_warehouse_moves():
    """Endpoint do pobierania wszystkich ruchów magazynowych."""
    warehouse_moves = get_all_warehouse_moves()
    return jsonify([str(move) for move in warehouse_moves])

@warehouse_move_blueprint.route('/warehouse_moves/<int:warehouse_move_id>', methods=['GET'])
def get_warehouse_move(warehouse_move_id):
    """Endpoint do pobierania jednego ruchu magazynowego po ID."""
    warehouse_move = get_warehouse_move_by_id(warehouse_move_id)
    if not warehouse_move:
        return jsonify({"error": "Warehouse move not found"}), 404
    return jsonify(str(warehouse_move))

@warehouse_move_blueprint.route('/warehouse_moves', methods=['POST'])
def create_warehouse_move():
    """Endpoint do dodawania nowego ruchu magazynowego."""
    data = request.json
    warehouse_move = add_warehouse_move(
        move_type=data['move_type'],
        order_date=data['order_date'],
        implementation_date=data['implementation_date'],
        user_id=data['user_id']
    )
    return jsonify({"message": "Warehouse move added", "warehouse_move": str(warehouse_move)}), 201

@warehouse_move_blueprint.route('/warehouse_moves/<int:warehouse_move_id>', methods=['PUT'])
def modify_warehouse_move(warehouse_move_id):
    """Endpoint do aktualizacji istniejącego ruchu magazynowego."""
    data = request.json
    warehouse_move = update_warehouse_move(warehouse_move_id, **data)
    if not warehouse_move:
        return jsonify({"error": "Warehouse move not found"}), 404
    return jsonify({"message": "Warehouse move updated", "warehouse_move": str(warehouse_move)})

@warehouse_move_blueprint.route('/warehouse_moves/<int:warehouse_move_id>', methods=['DELETE'])
def remove_warehouse_move(warehouse_move_id):
    """Endpoint do usuwania ruchu magazynowego."""
    success = delete_warehouse_move(warehouse_move_id)
    if not success:
        return jsonify({"error": "Warehouse move not found"}), 404
    return jsonify({"message": "Warehouse move deleted"})
