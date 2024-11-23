import os

class Config:
    """Podstawowa konfiguracja aplikacji"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Konfiguracja dla środowiska deweloperskiego"""
    DEBUG = True

class ProductionConfig(Config):
    """Konfiguracja dla środowiska produkcyjnego"""
    DEBUG = False