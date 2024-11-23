from models import db
from models.role import Role

def get_all_roles():
    """Pobiera wszystkie role."""
    return Role.query.all()

def get_role_by_id(role_id):
    """Pobiera rolę na podstawie ID."""
    return Role.query.get(role_id)

def add_role(role_name, permissions=None):
    """Dodaje nową rolę."""
    role = Role(
        role_name=role_name,
        permissions=permissions
    )
    db.session.add(role)
    db.session.commit()
    return role

def update_role(role_id, **kwargs):
    """Aktualizuje dane roli."""
    role = Role.query.get(role_id)
    if not role:
        return None

    for key, value in kwargs.items():
        if hasattr(role, key):
            setattr(role, key, value)
    
    db.session.commit()
    return role

def delete_role(role_id):
    """Usuwa rolę na podstawie ID."""
    role = Role.query.get(role_id)
    if not role:
        return False
    
    db.session.delete(role)
    db.session.commit()
    return True
