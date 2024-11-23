from flask import Blueprint
from .product_routes import product_blueprint
from .user_routes import user_blueprint
from .role_routes import role_blueprint
from .unit_routes import unit_blueprint
from .inventory_routes import inventory_blueprint
from .inventory_product_routes import inventory_product_blueprint
from .operation_log_routes import operation_log_blueprint
from .warehouse_move_routes import warehouse_move_blueprint
from .warehouse_move_product_routes import warehouse_move_product_blueprint

def register_blueprints(app):
    """
    Rejestruje wszystkie blueprinty w aplikacji Flask.
    """
    app.register_blueprint(product_blueprint, url_prefix='/api')
    app.register_blueprint(user_blueprint, url_prefix='/api')
    app.register_blueprint(role_blueprint, url_prefix='/api')
    app.register_blueprint(unit_blueprint, url_prefix='/api')
    app.register_blueprint(inventory_blueprint, url_prefix='/api')
    app.register_blueprint(inventory_product_blueprint, url_prefix='/api')
    app.register_blueprint(operation_log_blueprint, url_prefix='/api')
    app.register_blueprint(warehouse_move_blueprint, url_prefix='/api')
    app.register_blueprint(warehouse_move_product_blueprint, url_prefix='/api')
