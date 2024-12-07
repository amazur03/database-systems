import pytest
from app import app
from models import db
from models.unit import Unit

@pytest.fixture(scope='module')
def setup_database():
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_add_unit(setup_database):
    with app.app_context():
        unit = Unit(
            id="1",
            name="Tablet",
            percentage_of_the_stock=2
        )
        db.session.add(unit)
        db.session.commit()
        added_unit = Unit.query.filter_by(name="Tablet").first()
        assert added_unit is not None
        assert added_unit.name == "Tablet"
        assert added_unit.percentage_of_the_stock == 2.0
        print(f"Added Unit: id={added_unit.id}, name={added_unit.name}, percentage_of_the_stock={added_unit.percentage_of_the_stock}")

