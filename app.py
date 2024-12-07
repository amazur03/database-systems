from flask import Flask
from config import DevelopmentConfig  # Import konfiguracji
from models import init_app  # Import funkcji do inicjalizacji bazy danych
from routes import register_blueprints
from models.unit import Unit
import pytest
from models import db

# Tworzenie instancji aplikacji Flask
app = Flask(__name__)

# Ładowanie konfiguracji
app.config.from_object(DevelopmentConfig)

# Inicjalizacja bazy danych
init_app(app)

# Rejestracja blueprintów
register_blueprints(app)

###################################################################################################

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


test_add_unit(setup_database)
# Punkt wejścia do aplikacji
if __name__ == '__main__':
    app.run(debug=True)

