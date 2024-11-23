from flask import Blueprint, jsonify, request
from services.product_service import (
    get_all_products,
    get_product_by_id,
    add_product,
    update_product,
    delete_product
)

product_blueprint = Blueprint('products', __name__)

@product_blueprint.route('/products', methods=['GET'])
def list_products():
    """Endpoint do pobierania wszystkich produktów."""
    products = get_all_products()
    return jsonify([str(product) for product in products])

@product_blueprint.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Endpoint do pobierania jednego produktu po ID."""
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(str(product))

@product_blueprint.route('/products', methods=['POST'])
def create_product():
    """Endpoint do dodawania nowego produktu."""
    data = request.json
    product = add_product(
        name=data['name'],
        unit_id=data['unit_id'],
        max_stock=data['max_stock'],
        min_stock=data['min_stock'],
        current_stock=data['current_stock']
    )
    return jsonify({"message": "Product added", "product": str(product)}), 201

@product_blueprint.route('/products/<int:product_id>', methods=['PUT'])
def modify_product(product_id):
    """Endpoint do aktualizacji istniejącego produktu."""
    data = request.json
    product = update_product(product_id, **data)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"message": "Product updated", "product": str(product)})

@product_blueprint.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    """Endpoint do usuwania produktu."""
    success = delete_product(product_id)
    if not success:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"message": "Product deleted"})
