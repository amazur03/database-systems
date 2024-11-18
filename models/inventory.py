from app import db

class Inventory(db.Model):
    """
    Model for the 'inventory' table.
    This table stores inventory sessions with unique IDs and dates.
    """

    __tablename__ = 'inventory'

    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier for each inventory session
    date = db.Column(db.Date, nullable=False)  # Date of the inventory session


    inventory_products = db.relationship('InventoryProduct', back_populates='inventory')  # Relationship to inventory_products
    operation_logs = db.relationship('OperationLog', back_populates='inventory')  # Relationship to operation_logs

    def __repr__(self):
        """
        Provides a string representation of the Inventory instance.
        """
        return f"<Inventory(id={self.id}, date={self.date})>"
