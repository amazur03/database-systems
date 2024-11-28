from models import db

class WarehouseMoveProduct(db.Model):
    """
    Model for the 'warehouse_moves_products' table.
    This table links products to specific warehouse movements.
    """

    __tablename__ = 'warehouse_moves_products'

    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier for each warehouse movement-product link
    warehouse_move_id = db.Column(db.BigInteger, db.ForeignKey('warehouse_moves.id'), nullable=False)  # Foreign key to warehouse_moves
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'), nullable=False)  # Foreign key to products
    quantity = db.Column(db.BigInteger, nullable=False)  # Quantity moved in the warehouse movement


    warehouse_move = db.relationship('WarehouseMove', back_populates='warehouse_move_product')  # Relationship to warehouse_move
    product = db.relationship('Product', back_populates='warehouse_move_product')  # Relationship to product

    def __repr__(self):
        """
        Provides a string representation of the WarehouseMoveProduct instance.
        """
        return f"<WarehouseMoveProduct(id={self.id}, warehouse_move_id={self.warehouse_move_id}, product_id={self.product_id}, quantity={self.quantity})>"
