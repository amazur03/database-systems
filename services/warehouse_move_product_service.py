from models import db
from models.warehouse_move_product import WarehouseMoveProduct

def get_all_warehouse_move_products():
    """Pobiera wszystkie produkty związane z ruchami magazynowymi."""
    return WarehouseMoveProduct.query.all()

def get_warehouse_move_product_by_id(warehouse_move_product_id):
    """Pobiera produkt w ruchu magazynowym na podstawie ID."""
    return WarehouseMoveProduct.query.get(warehouse_move_product_id)

def add_warehouse_move_product(warehouse_move_id, product_id, quantity):
    """Dodaje produkt do ruchu magazynowego."""
    warehouse_move_product = WarehouseMoveProduct(
        warehouse_move_id=warehouse_move_id,
        product_id=product_id,
        quantity=quantity
    )
    db.session.add(warehouse_move_product)
    db.session.commit()
    return warehouse_move_product

def update_warehouse_move_product(warehouse_move_product_id, **kwargs):
    """Aktualizuje dane produktu w ruchu magazynowym."""
    warehouse_move_product = WarehouseMoveProduct.query.get(warehouse_move_product_id)
    if not warehouse_move_product:
        return None

    for key, value in kwargs.items():
        if hasattr(warehouse_move_product, key):
            setattr(warehouse_move_product, key, value)

    db.session.commit()
    return warehouse_move_product

def delete_warehouse_move_product(warehouse_move_product_id):
    """Usuwa produkt z ruchu magazynowego na podstawie ID."""
    warehouse_move_product = WarehouseMoveProduct.query.get(warehouse_move_product_id)
    if not warehouse_move_product:
        return False

    db.session.delete(warehouse_move_product)
    db.session.commit()
    return True
