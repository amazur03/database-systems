from flask import Blueprint, jsonify, request
from services.warehouse_move_product_service import (
    get_all_warehouse_move_products,
    get_warehouse_move_product_by_id,
    add_warehouse_move_product,
    update_warehouse_move_product,
    delete_warehouse_move_product
)

warehouse_move_product_blueprint = Blueprint('warehouse_move_products', __name__)

@warehouse_move_product_blueprint.route('/warehouse_move_products', methods=['GET'])
def list_warehouse_move_products():
    """Endpoint do pobierania wszystkich produktów w ruchach magazynowych."""
    warehouse_move_products = get_all_warehouse_move_products()
    return jsonify([str(product) for product in warehouse_move_products])

@warehouse_move_product_blueprint.route('/warehouse_move_products/<int:warehouse_move_product_id>', methods=['GET'])
def get_warehouse_move_product(warehouse_move_product_id):
    """Endpoint do pobierania jednego produktu w ruchu magazynowym po ID."""
    warehouse_move_product = get_warehouse_move_product_by_id(warehouse_move_product_id)
    if not warehouse_move_product:
        return jsonify({"error": "Warehouse move product not found"}), 404
    return jsonify(str(warehouse_move_product))

@warehouse_move_product_blueprint.route('/warehouse_move_products', methods=['POST'])
def create_warehouse_move_product():
    """Endpoint do dodawania produktu do ruchu magazynowego."""
    data = request.json
    warehouse_move_product = add_warehouse_move_product(
        warehouse_move_id=data['warehouse_move_id'],
        product_id=data['product_id'],
        quantity=data['quantity']
    )
    return jsonify({"message": "Warehouse move product added", "warehouse_move_product": str(warehouse_move_product)}), 201

@warehouse_move_product_blueprint.route('/warehouse_move_products/<int:warehouse_move_product_id>', methods=['PUT'])
def modify_warehouse_move_product(warehouse_move_product_id):
    """Endpoint do aktualizacji produktu w ruchu magazynowym."""
    data = request.json
    warehouse_move_product = update_warehouse_move_product(warehouse_move_product_id, **data)
    if not warehouse_move_product:
        return jsonify({"error": "Warehouse move product not found"}), 404
    return jsonify({"message": "Warehouse move product updated", "warehouse_move_product": str(warehouse_move_product)})

@warehouse_move_product_blueprint.route('/warehouse_move_products/<int:warehouse_move_product_id>', methods=['DELETE'])
def remove_warehouse_move_product(warehouse_move_product_id):
    """Endpoint do usuwania produktu z ruchu magazynowego."""
    success = delete_warehouse_move_product(warehouse_move_product_id)
    if not success:
        return jsonify({"error": "Warehouse move product not found"}), 404
    return jsonify({"message": "Warehouse move product deleted"})
