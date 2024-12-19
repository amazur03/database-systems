from flask_sqlalchemy import SQLAlchemy

# Tworzenie instancji SQLAlchemy
db = SQLAlchemy()

# Importowanie modeli
from .product import Product
from .user import User
from .unit import Unit
from .inventory import Inventory
from .inventory_product import InventoryProduct
from .operation_log import OperationLog
from .warehouse_move import WarehouseMove
from .warehouse_move_product import WarehouseMoveProduct
from .operation_log import OperationLog