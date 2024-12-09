from flask_admin.contrib.sqla import ModelView
from models import db, InventoryProduct, Inventory, Product, User
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import IntegerField, validators

class InventoryProductModelView(ModelView):
    """Admin view for the InventoryProduct model."""
    
    # Columns to be displayed in the list view (index view)
    column_list = ('id', 'inventory_id', 'product.name', 'counted_quantity', 'difference', 'user.username')

    # Columns to be included in the add/edit form
    form_columns = ('id', 'inventory_id', 'product', 'counted_quantity', 'user_id')  # Change product_name to product

    # Columns to be searchable in the list view
    column_searchable_list = ['inventory_id', 'product.name']  # Use product name

    # Columns that can be filtered in the list view
    column_filters = ['inventory_id', 'product.name', 'user.username']  # Use product name

    # Columns that are sortable
    column_sortable_list = ['inventory_id', 'product.name', 'counted_quantity', 'difference']  # Use product name

    # Extra fields for relationships with other models (Inventory, Product, and User)
    form_extra_fields = {
        'inventory_id': QuerySelectField(
            'Inventory',  # Label for the field
            query_factory=lambda: db.session.query(Inventory).all(),  # Fetch Inventory records
            widget=Select2Widget(),
            get_label=lambda inventory: f"ID: {inventory.id} - {inventory.date}"  # Show Inventory ID and Date in select
        ),
        'product': QuerySelectField(  # Changed to 'product' field
            'Product',  # Label for the field
            query_factory=lambda: db.session.query(Product).all(),  # Fetch Product records
            widget=Select2Widget(),
            get_label=lambda product: product.name  # Show product name in the select
        ),
        'user_id': QuerySelectField(
            'User',  # Label for the field
            query_factory=lambda: db.session.query(User).all(),  # Fetch User records
            widget=Select2Widget(),
            get_label=lambda user: user.username  # Show username in the select
        ),
    }

    # Formatter for displaying product name and user in a readable format
    column_formatters = {
        'user.username': lambda view, context, model, name: model.user.username if model.user else 'N/A',
        'product.name': lambda view, context, model, name: model.product.name if model.product else 'N/A',  # Correct field path
        'inventory.date': lambda view, context, model, name: model.inventory.date.strftime('%Y-%m-%d') if model.inventory else 'N/A',
    }

    # Custom validation for form fields
    form_args = {
        'counted_quantity': {
            'validators': [validators.InputRequired(), validators.NumberRange(min=0, message="Quantity must be greater than or equal to 0.")]
        }
    }

    # Logic before saving changes to the model
    def on_model_change(self, form, model, is_created):
        # Get the current stock quantity for the product
        product = db.session.query(Product).get(model.product_id)

        if product:
            # Calculate the difference between the counted quantity and the current stock
            model.difference = model.counted_quantity - product.current_stock  # Assuming `current_stock` is the field for the product's current stock
        else:
            model.difference = 0  # If product not found, set difference to 0

        # Continue with saving the model
        return super(InventoryProductModelView, self).on_model_change(form, model, is_created)

    # Prefill the form with existing model data (e.g., for editing an existing inventory product)
    def _on_form_prefill(self, form, id):
        inventory_product = db.session.query(InventoryProduct).get(id)
        if inventory_product:
            form.inventory_id.data = inventory_product.inventory_id
            form.product.data = inventory_product.product  # Use the actual Product object
            form.counted_quantity.data = inventory_product.counted_quantity
            form.user_id.data = inventory_product.user_id
        return super(InventoryProductModelView, self)._on_form_prefill(form, id)
