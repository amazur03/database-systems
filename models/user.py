from models import db # Import SQLAlchemy instance 'db' from the main app
from sqlalchemy.orm import validates # Import SQLAlchemy's validation decorator
import re # Import regex module to validate email format

class User(db.Model):
    """
    User model for storing user details in the 'users' table.
    This model includes fields such as username, password, name, surname, 
    email, and role_id, with email validation using regex.
    """
    
    __tablename__ = 'users'  # Defines the table name in the database

    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier for each user (primary key)
    username = db.Column(db.String, unique=True, nullable=False)  # Username, which must be unique and cannot be null
    password = db.Column(db.String, nullable=False)  # Password, stored as a string, cannot be null
    role_id = db.Column(db.BigInteger, db.ForeignKey('roles.id'), nullable=False)  # Foreign key referencing the roles table, defines the user's role
    name = db.Column(db.String, nullable=False)  # User's first name, cannot be null
    surname = db.Column(db.String, nullable=False)  # User's last name, cannot be null
    email = db.Column(db.String, unique=True, nullable=False)  # Email address, which must be unique and in a valid format

    operation_logs = db.relationship('OperationLog', back_populates='user', cascade="all, delete-orphan")
    roles = db.relationship('Role', back_populates='user', cascade="all, delete-orphan")  # Relationship with the Roles table - allows access to the role assigned to the user
    warehouse_moves = db.relationship('WarehouseMove', back_populates='user', cascade="all, delete-orphan")
    inventory_products = db.relationship('InventoryProduct', back_populates='user', cascade="all, delete-orphan")

    # Email verification using regex
    @validates('email')
    def validate_email(self, key, email):
        """
        Validates the email field to ensure it matches a standard email pattern.
        Raises a ValueError if the email format is invalid.
        """
        # Regex pattern for validating an email address
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
        # Check if email matches the pattern
        if not re.match(email_regex, email):
            raise ValueError("Invalid email address format")
        
        # Return the email if it passes validation
        return email

    def __repr__(self):
        """
        Provides a string representation of the User instance,
        showing the id, username, and email.
        """
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"