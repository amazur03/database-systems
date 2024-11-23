from flask import Blueprint, jsonify, request
from services.inventory_product_service import (
    get_all_inventory_products,
    get_inventory_product_by_id,
    add_inventory_product,
    update_inventory_product,
    delete_inventory_product
)

inventory_product_blueprint = Blueprint('inventory_products', __name__)

@inventory_product_blueprint.route('/inventory_products', methods=['GET'])
def list_inventory_products():
    """Endpoint do pobierania wszystkich produktów z sesji inwentaryzacyjnych."""
    inventory_products = get_all_inventory_products()
    return jsonify([str(inventory_product) for inventory_product in inventory_products])

@inventory_product_blueprint.route('/inventory_products/<int:inventory_product_id>', methods=['GET'])
def get_inventory_product(inventory_product_id):
    """Endpoint do pobierania jednego produktu z inwentaryzacji po ID."""
    inventory_product = get_inventory_product_by_id(inventory_product_id)
    if not inventory_product:
        return jsonify({"error": "Inventory product not found"}), 404
    return jsonify(str(inventory_product))

@inventory_product_blueprint.route('/inventory_products', methods=['POST'])
def create_inventory_product():
    """Endpoint do dodawania produktu do sesji inwentaryzacyjnej."""
    data = request.json
    inventory_product = add_inventory_product(
        inventory_id=data['inventory_id'],
        product_id=data['product_id'],
        counted_quantity=data['counted_quantity'],
        difference=data['difference'],
        user_id=data['user_id']
    )
    return jsonify({"message": "Inventory product added", "inventory_product": str(inventory_product)}), 201

@inventory_product_blueprint.route('/inventory_products/<int:inventory_product_id>', methods=['PUT'])
def modify_inventory_product(inventory_product_id):
    """Endpoint do aktualizacji produktu w sesji inwentaryzacyjnej."""
    data = request.json
    inventory_product = update_inventory_product(inventory_product_id, **data)
    if not inventory_product:
        return jsonify({"error": "Inventory product not found"}), 404
    return jsonify({"message": "Inventory product updated", "inventory_product": str(inventory_product)})

@inventory_product_blueprint.route('/inventory_products/<int:inventory_product_id>', methods=['DELETE'])
def remove_inventory_product(inventory_product_id):
    """Endpoint do usuwania produktu z sesji inwentaryzacyjnej."""
    success = delete_inventory_product(inventory_product_id)
    if not success:
        return jsonify({"error": "Inventory product not found"}), 404
    return jsonify({"message": "Inventory product deleted"})
