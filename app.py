from flask import Flask
from config import DevelopmentConfig  # Import konfiguracji
from models import init_app  # Import funkcji do inicjalizacji bazy danych
from routes import register_blueprints

# Tworzenie instancji aplikacji Flask
app = Flask(__name__)

# Ładowanie konfiguracji
app.config.from_object(DevelopmentConfig)

# Inicjalizacja bazy danych
init_app(app)

# Rejestracja blueprintów
register_blueprints(app)

# Punkt wejścia do aplikacji
if __name__ == '__main__':
    app.run(debug=True)
