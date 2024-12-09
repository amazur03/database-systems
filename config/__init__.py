from flask import Flask
from flask_migrate import Migrate
from models import db

import logging
logging.basicConfig(level=logging.INFO)

# Initialize the database object globally
migrate = Migrate()

def register_extensions(app):
    # Initialize the database with the app
    db.init_app(app)
    app.logger.info('Database initialized')

    # Initialize Flask-Migrate for database migrations
    migrate.init_app(app, db)
    app.logger.info('Migration initialized')

def configure_app(app):
    # Set the secret key to use for the session, change this later
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

def create_app():
    app = Flask(__name__)

    # Configure the app
    configure_app(app)
    app.logger.info('App configured successfully')

    try:
        # Register extensions
        register_extensions(app)
        app.logger.info('App created successfully')
        return app
    except Exception as e:
        app.logger.error(f'Error in creating app: {str(e)}')
        raise