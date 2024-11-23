from models import db

class InventoryProduct(db.Model):
    """
    Model for the 'inventory_products' table.
    This table links products to a specific inventory session with quantities and differences.
    """

    __tablename__ = 'inventory_products'

    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier for each inventory-product link
    inventory_id = db.Column(db.BigInteger, db.ForeignKey('inventory.id'), nullable=False)  # Foreign key to the inventory table
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'), nullable=False)  # Foreign key to the products table
    counted_quantity = db.Column(db.BigInteger, nullable=False)  # Quantity counted during inventory
    difference = db.Column(db.BigInteger, nullable=False)  # Difference between counted and current stock
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)  # Foreign key to the users table


    inventory = db.relationship('Inventory', back_populates='inventory_products')  # Relationship to inventory
    product = db.relationship('Product')  # Relationship to product
    user = db.relationship('User')  # Relationship to user



    def __repr__(self):
        """
        Provides a string representation of the InventoryProduct instance.
        """
        return f"<InventoryProduct(id={self.id}, inventory_id={self.inventory_id}, product_id={self.product_id}, counted_quantity={self.counted_quantity}, difference={self.difference}, user_id={self.user_id})>"
