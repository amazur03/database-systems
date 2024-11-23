from models import db
from models.inventory_product import InventoryProduct

def get_all_inventory_products():
    """Pobiera wszystkie produkty z sesji inwentaryzacyjnych."""
    return InventoryProduct.query.all()

def get_inventory_product_by_id(inventory_product_id):
    """Pobiera produkt z inwentaryzacji na podstawie ID."""
    return InventoryProduct.query.get(inventory_product_id)

def add_inventory_product(inventory_id, product_id, counted_quantity, difference, user_id):
    """Dodaje produkt do sesji inwentaryzacyjnej."""
    inventory_product = InventoryProduct(
        inventory_id=inventory_id,
        product_id=product_id,
        counted_quantity=counted_quantity,
        difference=difference,
        user_id=user_id
    )
    db.session.add(inventory_product)
    db.session.commit()
    return inventory_product

def update_inventory_product(inventory_product_id, **kwargs):
    """Aktualizuje dane produktu w inwentaryzacji."""
    inventory_product = InventoryProduct.query.get(inventory_product_id)
    if not inventory_product:
        return None
    
    for key, value in kwargs.items():
        if hasattr(inventory_product, key):
            setattr(inventory_product, key, value)
    
    db.session.commit()
    return inventory_product

def delete_inventory_product(inventory_product_id):
    """Usuwa produkt z sesji inwentaryzacyjnej."""
    inventory_product = InventoryProduct.query.get(inventory_product_id)
    if not inventory_product:
        return False
    
    db.session.delete(inventory_product)
    db.session.commit()
    return True
