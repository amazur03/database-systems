from models import db
from models.user import User

def get_all_users():
    """Pobiera wszystkich użytkowników."""
    return User.query.all()

def get_user_by_id(user_id):
    """Pobiera użytkownika na podstawie ID."""
    return User.query.get(user_id)

def add_user(username, password, name, surname, email, role_id):
    """Dodaje nowego użytkownika."""
    user = User(
        username=username,
        password=password,
        name=name,
        surname=surname,
        email=email,
        role_id=role_id
    )
    db.session.add(user)
    db.session.commit()
    return user

def update_user(user_id, **kwargs):
    """Aktualizuje dane użytkownika."""
    user = User.query.get(user_id)
    if not user:
        return None

    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.session.commit()
    return user

def delete_user(user_id):
    """Usuwa użytkownika na podstawie ID."""
    user = User.query.get(user_id)
    if not user:
        return False

    db.session.delete(user)
    db.session.commit()
    return True
