from flask import Blueprint, jsonify, request
from services.unit_service import (
    get_all_units,
    get_unit_by_id,
    add_unit,
    update_unit,
    delete_unit
)

unit_blueprint = Blueprint('units', __name__)

@unit_blueprint.route('/units', methods=['GET'])
def list_units():
    """Endpoint do pobierania wszystkich jednostek miary."""
    units = get_all_units()
    return jsonify([str(unit) for unit in units])

@unit_blueprint.route('/units/<int:unit_id>', methods=['GET'])
def get_unit(unit_id):
    """Endpoint do pobierania jednej jednostki miary po ID."""
    unit = get_unit_by_id(unit_id)
    if not unit:
        return jsonify({"error": "Unit not found"}), 404
    return jsonify(str(unit))

@unit_blueprint.route('/units', methods=['POST'])
def create_unit():
    """Endpoint do dodawania nowej jednostki miary."""
    data = request.json
    unit = add_unit(
        name=data['name'],
        percentage_of_the_stock=data.get('percentage_of_the_stock')
    )
    return jsonify({"message": "Unit added", "unit": str(unit)}), 201

@unit_blueprint.route('/units/<int:unit_id>', methods=['PUT'])
def modify_unit(unit_id):
    """Endpoint do aktualizacji istniejącej jednostki miary."""
    data = request.json
    unit = update_unit(unit_id, **data)
    if not unit:
        return jsonify({"error": "Unit not found"}), 404
    return jsonify({"message": "Unit updated", "unit": str(unit)})

@unit_blueprint.route('/units/<int:unit_id>', methods=['DELETE'])
def remove_unit(unit_id):
    """Endpoint do usuwania jednostki miary."""
    success = delete_unit(unit_id)
    if not success:
        return jsonify({"error": "Unit not found"}), 404
    return jsonify({"message": "Unit deleted"})
