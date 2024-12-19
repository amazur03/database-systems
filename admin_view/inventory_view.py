from flask_admin.contrib.sqla import ModelView
from models import db, Inventory, OperationLog
from flask_login import current_user
from sqlalchemy.event import listens_for
from datetime import datetime

class InventoryModelView(ModelView):
    """Admin view for the Inventory model."""
    column_list = ('id', 'description', 'date')
    form_columns = ('description', 'date')
    column_filters = ['date']
    column_searchable_list = ['description']
    column_sortable_list = ['id', 'description', 'date']

    column_labels = {
        'id': 'ID',
        'description': 'Description',
        'date': 'Date'
    }

    def is_accessible(self):
        # Check if the current user is authenticated and has 'admin' role
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for
        # Redirect unauthenticated or unauthorized users to the login page
        return redirect(url_for('login'))


# LISTENER FUNCTIONS
@listens_for(Inventory, 'after_insert')
def after_insert_inventory(mapper, connection, target):
    """Log operation after an Inventory record is inserted."""
    user_id = getattr(current_user, 'id', None)
    if not user_id:
        return
    log_entry = {
        "operation_type": 'INSERT',
        "user_id": user_id,
        "operation_model": 'Inventory',
        "operation_id": target.id,
        "details": f"Inventory created with description '{target.description}'",
        "timestamp": datetime.utcnow()
    }
    connection.execute(OperationLog.__table__.insert(), log_entry)


@listens_for(Inventory, 'after_update')
def after_update_inventory(mapper, connection, target):
    """Log operation after an Inventory record is updated."""
    user_id = getattr(current_user, 'id', None)
    if not user_id:
        return
    log_entry = {
        "operation_type": 'UPDATE',
        "user_id": user_id,
        "operation_model": 'Inventory',
        "operation_id": target.id,
        "details": f"Inventory updated with description '{target.description}'",
        "timestamp": datetime.utcnow()
    }
    connection.execute(OperationLog.__table__.insert(), log_entry)


@listens_for(Inventory, 'after_delete')
def after_delete_inventory(mapper, connection, target):
    """Log operation after an Inventory record is deleted."""
    user_id = getattr(current_user, 'id', None)
    if not user_id:
        return
    log_entry = {
        "operation_type": 'DELETE',
        "user_id": user_id,
        "operation_model": 'Inventory',
        "operation_id": target.id,
        "details": f"Inventory deleted with description '{target.description}'",
        "timestamp": datetime.utcnow()
    }
    connection.execute(OperationLog.__table__.insert(), log_entry)
