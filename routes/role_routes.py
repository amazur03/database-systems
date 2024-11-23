from flask import Blueprint, jsonify, request
from services.role_service import (
    get_all_roles,
    get_role_by_id,
    add_role,
    update_role,
    delete_role
)

role_blueprint = Blueprint('roles', __name__)

@role_blueprint.route('/roles', methods=['GET'])
def list_roles():
    """Endpoint do pobierania wszystkich ról."""
    roles = get_all_roles()
    return jsonify([str(role) for role in roles])

@role_blueprint.route('/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    """Endpoint do pobierania jednej roli po ID."""
    role = get_role_by_id(role_id)
    if not role:
        return jsonify({"error": "Role not found"}), 404
    return jsonify(str(role))

@role_blueprint.route('/roles', methods=['POST'])
def create_role():
    """Endpoint do dodawania nowej roli."""
    data = request.json
    role = add_role(
        role_name=data['role_name'],
        permissions=data.get('permissions')
    )
    return jsonify({"message": "Role added", "role": str(role)}), 201

@role_blueprint.route('/roles/<int:role_id>', methods=['PUT'])
def modify_role(role_id):
    """Endpoint do aktualizacji istniejącej roli."""
    data = request.json
    role = update_role(role_id, **data)
    if not role:
        return jsonify({"error": "Role not found"}), 404
    return jsonify({"message": "Role updated", "role": str(role)})

@role_blueprint.route('/roles/<int:role_id>', methods=['DELETE'])
def remove_role(role_id):
    """Endpoint do usuwania roli."""
    success = delete_role(role_id)
    if not success:
        return jsonify({"error": "Role not found"}), 404
    return jsonify({"message": "Role deleted"})
