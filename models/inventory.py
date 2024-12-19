from models import db

class Inventory(db.Model):
    """
    Model for the 'inventory' table.
    This table stores inventory sessions with unique IDs and dates.
    """

    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique identifier for each inventory session
    date = db.Column(db.Date, nullable=False)  # Date of the inventory session
    description = db.Column(db.String, nullable=False)

     # Relationship to InventoryProduct
    inventory_product = db.relationship('InventoryProduct', back_populates='inventory')

    # Relationship to OperationLog
    operation_logs = db.relationship('OperationLog', back_populates='inventory', cascade='all, delete-orphan')

    def __repr__(self):
        """
        Provides a string representation of the Inventory instance.
        """
        return f"<Inventory(id={self.id}, date={self.date})>"
