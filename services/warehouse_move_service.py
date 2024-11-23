from models import db
from models.warehouse_move import WarehouseMove

def get_all_warehouse_moves():
    """Pobiera wszystkie ruchy magazynowe."""
    return WarehouseMove.query.all()

def get_warehouse_move_by_id(warehouse_move_id):
    """Pobiera ruch magazynowy na podstawie ID."""
    return WarehouseMove.query.get(warehouse_move_id)

def add_warehouse_move(move_type, order_date, implementation_date, user_id):
    """Dodaje nowy ruch magazynowy."""
    warehouse_move = WarehouseMove(
        move_type=move_type,
        order_date=order_date,
        implementation_date=implementation_date,
        user_id=user_id
    )
    db.session.add(warehouse_move)
    db.session.commit()
    return warehouse_move

def update_warehouse_move(warehouse_move_id, **kwargs):
    """Aktualizuje dane ruchu magazynowego."""
    warehouse_move = WarehouseMove.query.get(warehouse_move_id)
    if not warehouse_move:
        return None

    for key, value in kwargs.items():
        if hasattr(warehouse_move, key):
            setattr(warehouse_move, key, value)

    db.session.commit()
    return warehouse_move

def delete_warehouse_move(warehouse_move_id):
    """Usuwa ruch magazynowy na podstawie ID."""
    warehouse_move = WarehouseMove.query.get(warehouse_move_id)
    if not warehouse_move:
        return False

    db.session.delete(warehouse_move)
    db.session.commit()
    return True
