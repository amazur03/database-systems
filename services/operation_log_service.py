from models import db
from models.operation_log import OperationLog
from datetime import datetime

def get_all_operation_logs():
    """Pobiera wszystkie logi operacji."""
    return OperationLog.query.all()

def get_operation_log_by_id(operation_log_id):
    """Pobiera log operacji na podstawie ID."""
    return OperationLog.query.get(operation_log_id)

def add_operation_log(operation_type, user_id, previous_value, new_value, warehouse_move_id=None, inventory_id=None, details=None):
    """Dodaje nowy log operacji."""
    operation_log = OperationLog(
        operation_type=operation_type,
        user_id=user_id,
        previous_value=previous_value,
        new_value=new_value,
        warehouse_move_id=warehouse_move_id,
        inventory_id=inventory_id,
        details=details,
        timestamp=datetime.utcnow()
    )
    db.session.add(operation_log)
    db.session.commit()
    return operation_log

def update_operation_log(operation_log_id, **kwargs):
    """Aktualizuje istniejący log operacji."""
    operation_log = OperationLog.query.get(operation_log_id)
    if not operation_log:
        return None

    for key, value in kwargs.items():
        if hasattr(operation_log, key):
            setattr(operation_log, key, value)

    db.session.commit()
    return operation_log

def delete_operation_log(operation_log_id):
    """Usuwa log operacji na podstawie ID."""
    operation_log = OperationLog.query.get(operation_log_id)
    if not operation_log:
        return False

    db.session.delete(operation_log)
    db.session.commit()
    return True
