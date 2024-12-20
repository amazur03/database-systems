from models import db
from sqlalchemy.orm import validates

class Product(db.Model):
    """
    Product model for storing product details in the 'products' table.
    This model includes fields such as name, unit_id, max stock, min stock, and current stock.
    """
    
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique identifier for each product (primary key)
    name = db.Column(db.String, nullable=False)  # Name of the product, cannot be null
    unit_id = db.Column(db.BigInteger, db.ForeignKey('units.id'), nullable=False)  # Foreign key referencing the units table
    max_stock = db.Column(db.BigInteger, nullable=False)  # Maximum stock quantity, cannot be null
    min_stock = db.Column(db.BigInteger, nullable=False)  # Minimum stock quantity, cannot be null
    current_stock = db.Column(db.BigInteger, nullable=False)  # Current stock quantity, cannot be null

    inventory_product = db.relationship('InventoryProduct', back_populates='product')
    unit = db.relationship('Unit', back_populates='product', single_parent=True, cascade='all', passive_deletes=True)
    warehouse_move_product = db.relationship('WarehouseMoveProduct', back_populates='product')
    operation_logs = db.relationship('OperationLog', back_populates='product', cascade='all, delete-orphan')


    def __repr__(self):
        """
        Provides a string representation of the Product instance.
        """
        return f"<Product(id={self.id}, name='{self.name}', current_stock={self.current_stock})>"