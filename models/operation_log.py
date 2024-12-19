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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operation_type = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    warehouse_move_id = db.Column(db.Integer, db.ForeignKey('warehouse_moves.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='operation_logs')
    inventory = db.relationship('Inventory', back_populates='operation_logs')
    warehouse_move = db.relationship('WarehouseMove', back_populates='operation_logs')
    product = db.relationship('Product', back_populates='operation_logs')

    def __repr__(self):
        """
        Provides a string representation of the OperationLog instance.
        """
        return f"<OperationLog(id={self.id}, operation_type='{self.operation_type}', timestamp='{self.timestamp}')>"