from flask import Blueprint, jsonify, request
from services.user_service import (
    get_all_users,
    get_user_by_id,
    add_user,
    update_user,
    delete_user
)

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/users', methods=['GET'])
def list_users():
    """Endpoint do pobierania wszystkich użytkowników."""
    users = get_all_users()
    return jsonify([str(user) for user in users])

@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Endpoint do pobierania jednego użytkownika po ID."""
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(str(user))

@user_blueprint.route('/users', methods=['POST'])
def create_user():
    """Endpoint do dodawania nowego użytkownika."""
    data = request.json
    user = add_user(
        username=data['username'],
        password=data['password'],
        name=data['name'],
        surname=data['surname'],
        email=data['email'],
        role_id=data['role_id']
    )
    return jsonify({"message": "User added", "user": str(user)}), 201

@user_blueprint.route('/users/<int:user_id>', methods=['PUT'])
def modify_user(user_id):
    """Endpoint do aktualizacji istniejącego użytkownika."""
    data = request.json
    user = update_user(user_id, **data)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User updated", "user": str(user)})

@user_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    """Endpoint do usuwania użytkownika."""
    success = delete_user(user_id)
    if not success:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"})
