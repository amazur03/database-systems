from models import db
from sqlalchemy.orm import validates
from datetime import datetime

class OperationLog(db.Model):
    """
    OperationLog model for storing operation log details in the 'operation_logs' table.
    This model includes fields such as operation type, user_id, warehouse_move_id, inventory_id,
    previous value, new value, timestamp, and details.
    """
    
    __tablename__ = 'operation_logs'

    id = db.Column(db.BigInteger, primary_key=True)  # Unique identifier for each operation log (primary key)
    operation_type = db.Column(db.String, nullable=False)  # Type of operation, cannot be null
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)  # Foreign key referencing the users table
    warehouse_move_id = db.Column(db.BigInteger, db.ForeignKey('warehouse_moves.id'), nullable=True)  # Nullable foreign key referencing warehouse moves
    inventory_id = db.Column(db.BigInteger, db.ForeignKey('inventory.id'), nullable=True)  # Nullable foreign key referencing inventory
    previous_value = db.Column(db.BigInteger, nullable=False)  # Previous value, cannot be null
    new_value = db.Column(db.BigInteger, nullable=False)  # New value, cannot be null
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Timestamp of the operation, defaults to current time
    details = db.Column(db.Text)  # Additional details for the operation

    user = db.relationship('User', back_populates='operation_log')  # Relationship with the Users table
    warehouse_move = db.relationship('WarehouseMove', back_populates='operation_log')  # Relationship with the WarehouseMoves table
    inventory = db.relationship('Inventory', back_populates='operation_log')  # Relationship with the Inventory table

    def __repr__(self):
        """
        Provides a string representation of the OperationLog instance.
        """
        return f"<OperationLog(id={self.id}, operation_type='{self.operation_type}', timestamp='{self.timestamp}')>"