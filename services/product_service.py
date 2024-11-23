from models import db
from models.product import Product

def get_all_products():
    """Pobiera wszystkie produkty."""
    return Product.query.all()

def get_product_by_id(product_id):
    """Pobiera produkt na podstawie ID."""
    return Product.query.get(product_id)

def add_product(name, unit_id, max_stock, min_stock, current_stock):
    """Dodaje nowy produkt."""
    product = Product(
        name=name,
        unit_id=unit_id,
        max_stock=max_stock,
        min_stock=min_stock,
        current_stock=current_stock
    )
    db.session.add(product)
    db.session.commit()
    return product

def update_product(product_id, **kwargs):
    """Aktualizuje dane produktu."""
    product = Product.query.get(product_id)
    if not product:
        return None

    for key, value in kwargs.items():
        if hasattr(product, key):
            setattr(product, key, value)
    
    db.session.commit()
    return product

def delete_product(product_id):
    """Usuwa produkt na podstawie ID."""
    product = Product.query.get(product_id)
    if not product:
        return False
    
    db.session.delete(product)
    db.session.commit()
    return True
