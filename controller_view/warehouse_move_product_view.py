from flask_admin.contrib.sqla import ModelView
from models import db, WarehouseMoveProduct, WarehouseMove, Product
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import IntegerField, validators
from flask_login import current_user
from flask_admin.babel import gettext

class ControllerWarehouseMoveProductModelView(ModelView):
    """Admin view for the WarehouseMoveProduct model."""
    column_list = ('id', 'warehouse_move.move_type', 'product.name', 'quantity')
    form_columns = ('warehouse_move', 'product', 'quantity')
    column_filters = ['warehouse_move.move_type', 'product.name']
    column_searchable_list = ['warehouse_move.move_type', 'product.name']
    column_sortable_list = ['id', 'warehouse_move.move_type', 'product.name', 'quantity']
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

    column_labels = {
        'id': 'ID',
        'warehouse_move.move_type': 'Move Type',
        'product.name': 'Product Name',
        'quantity': 'Quantity'
    }

    can_create = True
    can_edit = True
    can_delete = False
    
    def on_model_change(self, form, model, is_created):
        """Override the model change to update product stock."""
        if is_created:
            warehouse_move = model.warehouse_move
            product = model.product

            new_stock = product.current_stock
            if warehouse_move.move_type == 'IN':
                new_stock += model.quantity
            elif warehouse_move.move_type == 'OUT':
                new_stock -= model.quantity

            if new_stock < 0:
                raise ValueError(
                    gettext(
                        "Insufficient stock for product '%(product_name)s'. Current stock: %(current_stock)d, attempted to deduct: %(quantity)d.",
                        product_name=product.name,
                        current_stock=product.current_stock,
                        quantity=model.quantity
                    )
                )

            product.current_stock = new_stock
            db.session.commit()

        return super(ControllerWarehouseMoveProductModelView, self).on_model_change(form, model, is_created)

    def _on_form_prefill(self, form, id):
        return super(ControllerWarehouseMoveProductModelView, self)._on_form_prefill(form, id)
    
    def is_accessible(self):
        # Check if the current user is authenticated and has 'admin' role
        return current_user.is_authenticated and current_user.role == 'controller'

    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for
        # Redirect unauthenticated or unauthorized users to the login page
        return redirect(url_for('login'))