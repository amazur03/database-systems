from flask import Blueprint, jsonify, request
from services.operation_log_service import (
    get_all_operation_logs,
    get_operation_log_by_id,
    add_operation_log,
    update_operation_log,
    delete_operation_log
)

operation_log_blueprint = Blueprint('operation_logs', __name__)

@operation_log_blueprint.route('/operation_logs', methods=['GET'])
def list_operation_logs():
    """Endpoint do pobierania wszystkich logów operacji."""
    operation_logs = get_all_operation_logs()
    return jsonify([str(log) for log in operation_logs])

@operation_log_blueprint.route('/operation_logs/<int:operation_log_id>', methods=['GET'])
def get_operation_log(operation_log_id):
    """Endpoint do pobierania jednego logu operacji po ID."""
    operation_log = get_operation_log_by_id(operation_log_id)
    if not operation_log:
        return jsonify({"error": "Operation log not found"}), 404
    return jsonify(str(operation_log))

@operation_log_blueprint.route('/operation_logs', methods=['POST'])
def create_operation_log():
    """Endpoint do dodawania nowego logu operacji."""
    data = request.json
    operation_log = add_operation_log(
        operation_type=data['operation_type'],
        user_id=data['user_id'],
        previous_value=data['previous_value'],
        new_value=data['new_value'],
        warehouse_move_id=data.get('warehouse_move_id'),
        inventory_id=data.get('inventory_id'),
        details=data.get('details')
    )
    return jsonify({"message": "Operation log added", "operation_log": str(operation_log)}), 201

@operation_log_blueprint.route('/operation_logs/<int:operation_log_id>', methods=['PUT'])
def modify_operation_log(operation_log_id):
    """Endpoint do aktualizacji istniejącego logu operacji."""
    data = request.json
    operation_log = update_operation_log(operation_log_id, **data)
    if not operation_log:
        return jsonify({"error": "Operation log not found"}), 404
    return jsonify({"message": "Operation log updated", "operation_log": str(operation_log)})

@operation_log_blueprint.route('/operation_logs/<int:operation_log_id>', methods=['DELETE'])
def remove_operation_log(operation_log_id):
    """Endpoint do usuwania logu operacji."""
    success = delete_operation_log(operation_log_id)
    if not success:
        return jsonify({"error": "Operation log not found"}), 404
    return jsonify({"message": "Operation log deleted"})
