from flask import Blueprint, jsonify, request
from services.inventory_service import (
    get_all_inventories,
    get_inventory_by_id,
    add_inventory,
    update_inventory,
    delete_inventory
)

inventory_blueprint = Blueprint('inventory', __name__)

@inventory_blueprint.route('/inventories', methods=['GET'])
def list_inventories():
    """Endpoint do pobierania wszystkich sesji inwentaryzacyjnych."""
    inventories = get_all_inventories()
    return jsonify([str(inventory) for inventory in inventories])

@inventory_blueprint.route('/inventories/<int:inventory_id>', methods=['GET'])
def get_inventory(inventory_id):
    """Endpoint do pobierania jednej sesji inwentaryzacyjnej po ID."""
    inventory = get_inventory_by_id(inventory_id)
    if not inventory:
        return jsonify({"error": "Inventory not found"}), 404
    return jsonify(str(inventory))

@inventory_blueprint.route('/inventories', methods=['POST'])
def create_inventory():
    """Endpoint do dodawania nowej sesji inwentaryzacyjnej."""
    data = request.json
    inventory = add_inventory(date=data['date'])
    return jsonify({"message": "Inventory session added", "inventory": str(inventory)}), 201

@inventory_blueprint.route('/inventories/<int:inventory_id>', methods=['PUT'])
def modify_inventory(inventory_id):
    """Endpoint do aktualizacji sesji inwentaryzacyjnej."""
    data = request.json
    inventory = update_inventory(inventory_id, date=data.get('date'))
    if not inventory:
        return jsonify({"error": "Inventory not found"}), 404
    return jsonify({"message": "Inventory session updated", "inventory": str(inventory)})

@inventory_blueprint.route('/inventories/<int:inventory_id>', methods=['DELETE'])
def remove_inventory(inventory_id):
    """Endpoint do usuwania sesji inwentaryzacyjnej."""
    success = delete_inventory(inventory_id)
    if not success:
        return jsonify({"error": "Inventory not found"}), 404
    return jsonify({"message": "Inventory session deleted"})
