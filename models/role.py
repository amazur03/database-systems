from app import db  # Import SQLAlchemy instance 'db' from the main app

class Role(db.Model):
    """
    Role model for storing role details in the 'roles' table.
    This model includes fields such as role_name and permissions,
    and establishes a relationship with the User model.
    """

    __tablename__ = 'roles'  # Defines the table name in the database

    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier for each role (primary key)
    role_name = db.Column(db.String, unique=True, nullable=False)  # Role name, must be unique and cannot be null
    permissions = db.Column(db.Binary, nullable=True)  # Permissions stored in binary format, optional field

    users = db.relationship('User', back_populates='role', lazy='dynamic')  # Relationship with the User model; allows access to users assigned to this role

    def __repr__(self):
        """
        Provides a string representation of the Role instance,
        showing the id and role_name.
        """
        return f"<Role(id={self.id}, role_name='{self.role_name}')>"
