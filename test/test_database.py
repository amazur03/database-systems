import pytest
from app import app  # Import aplikacji Flask
from models import db  # Import bazy danych
import pytest
from models import Product

@pytest.fixture
def client():
    with app.app_context():
        db.create_all()  # Tworzy tabele przed każdym testem
        yield app.test_client()  # Udostępnia klienta testowego
        db.drop_all()  # Usuwa tabele po zakończeniu testu

def test_add_product(client):
    product = Product(name="Tablet", quantity=5)
    db.session.add(product)
    db.session.commit()
    assert Product.query.count() == 1

def test_delete_product(client):
    product = Product.query.first()
    db.session.delete(product)
    db.session.commit()
    assert Product.query.count() == 0
