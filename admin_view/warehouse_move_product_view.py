from flask_admin.contrib.sqla import ModelView
from models import db, WarehouseMoveProduct, WarehouseMove, Product
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import IntegerField, validators
from flask_login import current_user

class WarehouseMoveProductModelView(ModelView):
    """Admin view for the WarehouseMoveProduct model."""
    column_list = ('id', 'warehouse_move.move_type', 'product.name', 'quantity')
    form_columns = ('warehouse_move', 'product', 'quantity')
    column_filters = ['warehouse_move.move_type', 'product.name']
    column_searchable_list = ['warehouse_move.move_type', 'product.name']
    column_sortable_list = ['warehouse_move.move_type', 'product.name', 'quantity']
    form_extra_fields = {
        'warehouse_move': QuerySelectField(
            'Warehouse Move',
            query_factory=lambda: db.session.query(WarehouseMove).all(),
            widget=Select2Widget(),
            get_label=lambda warehouse_move: f"{warehouse_move.id} ({warehouse_move.move_type}, {warehouse_move.order_date})"
        ),
        'product': QuerySelectField(
            'Product',
            query_factory=lambda: db.session.query(Product).all(),
            widget=Select2Widget(),
            get_label=lambda product: product.name
        ),
        'quantity': IntegerField(
            'Quantity',
            validators=[validators.InputRequired(), validators.NumberRange(min=1)]
        ),
    }
    column_formatters = {
        'warehouse_move.move_type': lambda view, context, model, name: model.warehouse_move.move_type if model.warehouse_move else 'N/A',
        'product.name': lambda view, context, model, name: model.product.name if model.product else 'N/A',
        'quantity': lambda view, context, model, name: model.quantity if model.quantity else 'N/A'
    }
    form_args = {
        'quantity': {
            'validators': [validators.InputRequired(), validators.NumberRange(min=1)]
        }
    }

    def on_model_change(self, form, model, is_created):
        return super(WarehouseMoveProductModelView, self).on_model_change(form, model, is_created)

    def _on_form_prefill(self, form, id):
        return super(WarehouseMoveProductModelView, self)._on_form_prefill(form, id)

    def is_accessible(self):
        # Check if the current user is authenticated and has 'admin' role
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for
        # Redirect unauthenticated or unauthorized users to the login page
        return redirect(url_for('login'))