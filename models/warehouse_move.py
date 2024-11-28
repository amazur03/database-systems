from models import db
from sqlalchemy.orm import validates

class WarehouseMove(db.Model):
    """
    WarehouseMove model for storing warehouse movement details in the 'warehouse_moves' table.
    This model includes fields such as move type, order date, implementation date, and user_id.
    """
    
    __tablename__ = 'warehouse_moves'

    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier for each move (primary key)
    move_type = db.Column(db.String, nullable=False)  # Type of movement, cannot be null
    order_date = db.Column(db.Date, nullable=False)  # Order date, cannot be null
    implementation_date = db.Column(db.Date, nullable=False)  # Implementation date, cannot be null
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)  # Foreign key referencing the users table

    operation_logs = db.relationship('OperationLog', back_populates='warehouse_move', cascade="all, delete-orphan")
    users = db.relationship('User', back_populates='warehouse_moves', cascade="all, delete-orphan")  # Relationship with the Users table
    werahouse_move_products = db.relationship('WarehouseMoveProduct', back_populates='warehouse_move', cascade="all, delete-orphan")

    def __repr__(self):
        """
        Provides a string representation of the WarehouseMove instance.
        """
        return f"<WarehouseMove(id={self.id}, move_type='{self.move_type}', order_date='{self.order_date}')>"