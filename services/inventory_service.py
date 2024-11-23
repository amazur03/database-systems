from models import db
from models.inventory import Inventory

def get_all_inventories():
    """Pobiera wszystkie sesje inwentaryzacyjne."""
    return Inventory.query.all()

def get_inventory_by_id(inventory_id):
    """Pobiera sesję inwentaryzacyjną na podstawie ID."""
    return Inventory.query.get(inventory_id)

def add_inventory(date):
    """Dodaje nową sesję inwentaryzacyjną."""
    inventory = Inventory(date=date)
    db.session.add(inventory)
    db.session.commit()
    return inventory

def update_inventory(inventory_id, date=None):
    """Aktualizuje datę sesji inwentaryzacyjnej."""
    inventory = Inventory.query.get(inventory_id)
    if not inventory:
        return None
    
    if date:
        inventory.date = date
    
    db.session.commit()
    return inventory

def delete_inventory(inventory_id):
    """Usuwa sesję inwentaryzacyjną."""
    inventory = Inventory.query.get(inventory_id)
    if not inventory:
        return False

    db.session.delete(inventory)
    db.session.commit()
    return True
