from flask_admin.contrib.sqla import ModelView
from models import db, InventoryProduct, Inventory, Product, User
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import IntegerField, validators
from flask_login import current_user

class ControllerInventoryProductModelView(ModelView):
    """Admin view for the InventoryProduct model."""

    # Columns to be displayed in the list view (index view)
    column_list = ('id', 'inventory', 'product', 'counted_quantity', 'difference', 'user')

    # Columns to be included in the add/edit form
    form_columns = ('inventory', 'product', 'counted_quantity', 'user')

    # Columns to be searchable in the list view
    column_searchable_list = ['inventory.id', 'product.name']

    # Columns that can be filtered in the list view
    column_filters = ['inventory.id', 'product.name', 'user.username']

    # Columns that are sortable
    column_sortable_list = ['id', 'inventory', 'product', 'counted_quantity', 'difference', 'user']

    column_labels = {
        'id': 'ID',
        'inventory': 'Inventory',
        'product': 'Product',
        'counted_quantity': 'Counted Quantity',
        'difference': 'Difference',
        'user': 'User'
    }

    # Extra fields for relationships with other models (Inventory, Product, and User)
    form_extra_fields = {
        'inventory': QuerySelectField(
            'Inventory',
            query_factory=lambda: db.session.query(Inventory).order_by(Inventory.date.desc()).all(),
            widget=Select2Widget(),
            get_label=lambda inventory: f"ID: {inventory.id} - {inventory.description} ({inventory.date})"
        ),
        'product': QuerySelectField(
            'Product',
            query_factory=lambda: db.session.query(Product).order_by(Product.name).all(),
            widget=Select2Widget(),
            get_label=lambda product: product.name
        ),
        'user': QuerySelectField(
            'User',
            query_factory=lambda: db.session.query(User).order_by(User.username).all(),
            widget=Select2Widget(),
            get_label=lambda user: user.username
        )
    }

    # Formatter for displaying product name and user in a readable format
    column_formatters = {
        'user': lambda view, context, model, name: model.user.username if model.user else 'N/A',
        'product': lambda view, context, model, name: model.product.name if model.product else 'N/A',
        'inventory': lambda view, context, model, name: model.inventory.date.strftime('%Y-%m-%d') if model.inventory else 'N/A',
    }

    # Custom validation for form fields
    form_args = {
        'counted_quantity': {
            'validators': [validators.InputRequired(), validators.NumberRange(min=0, message="Quantity must be greater than or equal to 0.")]
        }
    }

    # Logic before saving changes to the model
    def on_model_change(self, form, model, is_created):
        # Fetch product by its ID (this assumes the product is already selected in the form)
        product = model.product
        if not product:
            raise ValueError("Selected product does not exist.")
        
        # Calculate the difference between counted and current stock
        model.difference = model.counted_quantity - product.current_stock

        # Proceed with saving the changes
        return super(ControllerInventoryProductModelView, self).on_model_change(form, model, is_created)

    # Prefill the form with existing model data (e.g., for editing an existing inventory product)
    def _on_form_prefill(self, form, id):
        # Fetch the InventoryProduct instance
        inventory_product = db.session.query(InventoryProduct).get(id)
        if inventory_product:
            # Prefill the form fields with the existing data
            form.inventory.data = inventory_product.inventory
            form.product.data = inventory_product.product
            form.counted_quantity.data = inventory_product.counted_quantity
            form.user.data = inventory_product.user
        return super(ControllerInventoryProductModelView, self)._on_form_prefill(form, id)
    
    def is_accessible(self):
        # Check if the current user is authenticated and has 'admin' role
        return current_user.is_authenticated and current_user.role == 'controller'

    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for
        # Redirect unauthenticated or unauthorized users to the login page
        return redirect(url_for('login'))