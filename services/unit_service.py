from models import db
from models.unit import Unit

def get_all_units():
    """Pobiera wszystkie jednostki miary."""
    return Unit.query.all()

def get_unit_by_id(unit_id):
    """Pobiera jednostkę miary na podstawie ID."""
    return Unit.query.get(unit_id)

def add_unit(name, percentage_of_the_stock=None):
    """Dodaje nową jednostkę miary."""
    unit = Unit(
        name=name,
        percentage_of_the_stock=percentage_of_the_stock
    )
    db.session.add(unit)
    db.session.commit()
    return unit

def update_unit(unit_id, **kwargs):
    """Aktualizuje dane jednostki miary."""
    unit = Unit.query.get(unit_id)
    if not unit:
        return None

    for key, value in kwargs.items():
        if hasattr(unit, key):
            setattr(unit, key, value)
    
    db.session.commit()
    return unit

def delete_unit(unit_id):
    """Usuwa jednostkę miary na podstawie ID."""
    unit = Unit.query.get(unit_id)
    if not unit:
        return False
    
    db.session.delete(unit)
    db.session.commit()
    return True
