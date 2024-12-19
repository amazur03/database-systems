from flask_admin.contrib.sqla import ModelView
from models import db, Product, Unit, OperationLog
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login import current_user
from sqlalchemy.event import listens_for
from datetime import datetime

class ProductModelView(ModelView):
    """Admin view for the Product model"""
    column_list = ('id', 'name', 'unit.name', 'max_stock', 'min_stock', 'current_stock')
    form_columns = ('name', 'unit', 'max_stock', 'min_stock', 'current_stock')
    form_extra_fields = {
        'unit': QuerySelectField(
            'Unit',
            query_factory=lambda: db.session.query(Unit).all(),
            widget=Select2Widget(),
            get_label=lambda unit: f"{unit.name} ({unit.percentage_of_the_stock:.2f}%)"
        )
    }
    column_searchable_list = ['name']
    column_sortable_list = ['id', 'name', 'unit.name', 'max_stock', 'min_stock', 'current_stock']
    column_formatters = {
        'unit.name': lambda view, context, model, name: f"{model.unit.name} ({model.unit.percentage_of_the_stock:.2f}%)" if model.unit else 'N/A'
    }
    column_filters = ['unit.name', 'current_stock']
    form_labels = {
        'name': 'Product Name',
        'unit': 'Unit',
        'max_stock': 'Maximum Stock',
        'min_stock': 'Minimum Stock',
        'current_stock': 'Current Stock'
    }

    column_labels = {
        'id': 'ID',
        'name': 'Product Name',
        'unit.name': 'Unit',
        'max_stock': 'Maximum Stock',
        'min_stock': 'Minimum Stock',
        'current_stock': 'Current Stock'
    }

    def is_accessible(self):
        # Check if the current user is authenticated and has 'admin' role
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for
        # Redirect unauthenticated or unauthorized users to the login page
        return redirect(url_for('login'))


# LISTENER FUNCTIONS
@listens_for(Product, 'after_insert')
def after_insert_product(mapper, connection, target):
    """Log operation after a Product record is inserted."""
    user_id = getattr(current_user, 'id', None)
    if not user_id:
        return
    log_entry = {
        "operation_type": 'INSERT',
        "user_id": user_id,
        "operation_model": 'Product',
        "operation_id": target.id,
        "details": f"Product created with name '{target.name}'",
        "timestamp": datetime.utcnow()
    }
    connection.execute(OperationLog.__table__.insert(), log_entry)


@listens_for(Product, 'after_update')
def after_update_product(mapper, connection, target):
    """Log operation after a Product record is updated."""
    user_id = getattr(current_user, 'id', None)
    if not user_id:
        return
    log_entry = {
        "operation_type": 'UPDATE',
        "user_id": user_id,
        "operation_model": 'Product',
        "operation_id": target.id,
        "details": f"Product updated with name '{target.name}'",
        "timestamp": datetime.utcnow()
    }
    connection.execute(OperationLog.__table__.insert(), log_entry)


@listens_for(Product, 'after_delete')
def after_delete_product(mapper, connection, target):
    """Log operation after a Product record is deleted."""
    user_id = getattr(current_user, 'id', None)
    if not user_id:
        return
    log_entry = {
        "operation_type": 'DELETE',
        "user_id": user_id,
        "operation_model": 'Product',
        "operation_id": target.id,
        "details": f"Product deleted with name '{target.name}'",
        "timestamp": datetime.utcnow()
    }
    connection.execute(OperationLog.__table__.insert(), log_entry)
