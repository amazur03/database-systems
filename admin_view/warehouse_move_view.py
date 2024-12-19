from flask_admin.contrib.sqla import ModelView
from models import db, WarehouseMove, User, OperationLog
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import SelectField, validators
from flask_login import current_user
from sqlalchemy.event import listens_for
from datetime import datetime

class WarehouseMoveModelView(ModelView):
    """Admin view for the WarehouseMove model."""
    column_list = ('id', 'move_type', 'order_date', 'implementation_date', 'user.username')
    form_columns = ('move_type', 'order_date', 'implementation_date', 'user')
    column_filters = ['move_type', 'order_date', 'implementation_date', 'user.username']
    column_searchable_list = ['move_type', 'user.username']
    column_sortable_list = ['move_type', 'order_date', 'implementation_date']
    form_extra_fields = {
        'user': QuerySelectField(
            'User',
            query_factory=lambda: db.session.query(User).all(),
            widget=Select2Widget(),
            get_label=lambda user: user.username
        ),
        'move_type': SelectField(
            'Move Type',
            choices=[('IN', 'IN'), ('OUT', 'OUT')],
            validators=[validators.InputRequired()]
        ),
    }
    column_formatters = {
        'user.username': lambda view, context, model, name: model.user.username if model.user else 'N/A',
        'order_date': lambda view, context, model, name: model.order_date.strftime('%Y-%m-%d') if model.order_date else 'N/A',
        'implementation_date': lambda view, context, model, name: model.implementation_date.strftime('%Y-%m-%d') if model.implementation_date else 'N/A'
    }
    form_args = {
        'order_date': {
            'validators': [validators.InputRequired()]
        },
        'implementation_date': {
            'validators': [validators.InputRequired()]
        }
    }

    def is_accessible(self):
        # Check if the current user is authenticated and has 'admin' role
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for
        # Redirect unauthenticated or unauthorized users to the login page
        return redirect(url_for('login'))


# LISTENER FUNCTIONS
@listens_for(WarehouseMove, 'after_insert')
def after_insert_warehouse_move(mapper, connection, target):
    """Log operation after a WarehouseMove record is inserted."""
    user_id = getattr(current_user, 'id', None)
    if not user_id:
        return
    log_entry = {
        "operation_type": 'INSERT',
        "user_id": user_id,
        "operation_model": 'WarehouseMove',
        "operation_id": target.id,
        "details": f"Warehouse move created with move type '{target.move_type}'",
        "timestamp": datetime.utcnow()
    }
    connection.execute(OperationLog.__table__.insert(), log_entry)


@listens_for(WarehouseMove, 'after_update')
def after_update_warehouse_move(mapper, connection, target):
    """Log operation after a WarehouseMove record is updated."""
    user_id = getattr(current_user, 'id', None)
    if not user_id:
        return
    log_entry = {
        "operation_type": 'UPDATE',
        "user_id": user_id,
        "operation_model": 'WarehouseMove',
        "operation_id": target.id,
        "details": f"Warehouse move updated with move type '{target.move_type}'",
        "timestamp": datetime.utcnow()
    }
    connection.execute(OperationLog.__table__.insert(), log_entry)


@listens_for(WarehouseMove, 'after_delete')
def after_delete_warehouse_move(mapper, connection, target):
    """Log operation after a WarehouseMove record is deleted."""
    user_id = getattr(current_user, 'id', None)
    if not user_id:
        return
    log_entry = {
        "operation_type": 'DELETE',
        "user_id": user_id,
        "operation_model": 'WarehouseMove',
        "operation_id": target.id,
        "details": f"Warehouse move deleted with move type '{target.move_type}'",
        "timestamp": datetime.utcnow()
    }
    connection.execute(OperationLog.__table__.insert(), log_entry)
