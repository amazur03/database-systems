from flask_admin.contrib.sqla import ModelView
from models import db, Unit, Role, Product, User
from flask_admin import expose
from flask_admin.base import BaseView
from flask import redirect, url_for
from flask_admin import form
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_admin.form.widgets import Select2Widget
from wtforms import PasswordField


class RoleModelView(ModelView):
    """Admin view for the Role model, accessible only to users with the 'admin' role."""

    # Columns displayed in the list view (index view)
    column_list = ('id', 'role_name', 'permission')

    # Columns that are editable in the add/edit form
    form_columns = ('id', 'role_name', 'permission')

    # Optional: Adding filtering capabilities in the admin panel
    column_filters = ['role_name']  # Allows filtering by role_name
    column_searchable_list = ['role_name']  # Enables searching by role_name

    # Optional: Format the 'permission' column to display it as a string instead of binary data
    column_formatters = {
        'permission': lambda view, context, model, name: 
            model.permission.decode('utf-8') if model.permission else 'None'  # Decode binary to string
    }


class UnitModelView(ModelView):
    """Admin view for the Unit model."""

    # Columns displayed in the list view (index view)
    column_list = ('id', 'name', 'percentage_of_the_stock')

    # Columns that are editable in the add/edit form
    form_columns = ('id', 'name', 'percentage_of_the_stock')

    # Optional: Adding filtering capabilities in the admin panel
    column_filters = ['name']  # Allows filtering by name
    column_searchable_list = ['name']  # Enables searching by name

    # Optional: Format the 'percentage_of_the_stock' column to display it as a percentage
    column_formatters = {
        'percentage_of_the_stock': lambda view, context, model, name: 
            f"{model.percentage_of_the_stock:.2f}%" if model.percentage_of_the_stock is not None else 'N/A'
    }

class ProductModelView(ModelView):
    """Admin view for the Product model"""

    # Columns displayed in the list view
    column_list = ('id', 'name', 'unit.name', 'max_stock', 'min_stock', 'current_stock')

    # Columns editable in the form
    form_columns = ('id', 'name', 'unit', 'max_stock', 'min_stock', 'current_stock')

    # Define a custom form with QuerySelectField for 'unit'
    form_extra_fields = {
        'unit': QuerySelectField(
            'Unit',  # Label for the field
            query_factory=lambda: db.session.query(Unit).all(),  # Loading units from the database
            widget=Select2Widget(),  # Use Select2Widget for better UI
            get_label=lambda unit: f"{unit.name} ({unit.percentage_of_the_stock:.2f}%)"  # Display unit with percentage
        )
    }

    # Columns searchable in the list view
    column_searchable_list = ['name']

    # Columns that are sortable in the list view
    column_sortable_list = ['name', 'current_stock']

    # Format the 'unit' column in the form view
    column_formatters = {
        'unit.name': lambda view, context, model, name: f"{model.unit.name} ({model.unit.percentage_of_the_stock:.2f}%)" if model.unit else 'N/A'
    }

    # Filters in the list view
    column_filters = ['unit.name', 'current_stock']

    # Optional: If you want to change the labels or add more fields to the form
    form_labels = {
        'name': 'Product Name',
        'unit': 'Unit',
        'max_stock': 'Maximum Stock',
        'min_stock': 'Minimum Stock',
        'current_stock': 'Current Stock'
    }

class UserModelView(ModelView):
    """Admin view for the User model"""

    # Columns displayed in the list view
    column_list = ('id', 'username', 'name', 'surname', 'email', 'role.role_name')  # Corrected to 'role.role_name'

    # Columns editable in the form
    form_columns = ('id', 'username', 'password', 'role', 'name', 'surname', 'email')

    # Use a form with QuerySelectField for the 'role' field
    form_extra_fields = {
        'role': QuerySelectField(
            'Role',  # Label for the field
            query_factory=lambda: db.session.query(Role).all(),  # Loading roles from the database
            widget=Select2Widget(),  # Use Select2Widget for better UI
            get_label=lambda role: role.role_name  # Corrected to 'role_name'
        ),
        'password': PasswordField('Password')  # Allow password entry
    }

    # Columns searchable in the list view
    column_searchable_list = ['username', 'email', 'name', 'surname']

    # Columns that are sortable in the list view
    column_sortable_list = ['username', 'name', 'email']

    # Format columns, e.g., for user role
    column_formatters = {
        'role.role_name': lambda view, context, model, name: model.role.role_name if model.role else 'N/A'  # Corrected to 'role.role_name'
    }

    # Filters in the list view
    column_filters = ['role.role_name', 'email']  # Corrected to 'role.role_name'

    # Labels for columns in the form
    form_labels = {
        'username': 'Username',
        'name': 'First Name',
        'surname': 'Last Name',
        'email': 'Email Address',
        'role': 'Role',
        'password': 'Password'
    }

    # Enable or disable options for specific fields (e.g., password field)
    form_widget_args = {
        'password': {
            'type': 'password'  # Set field type to 'password' for security
        }
    }

    # Modify form data before saving changes
    def on_model_change(self, form, model, is_created):
        """Before committing the changes to the database"""
        if is_created:
            model.password = form.password.data  # Save password from the form
            # Password can be hashed (e.g., using bcrypt) before saving to the database
        return super(UserModelView, self).on_model_change(form, model, is_created)

    def _on_form_prefill(self, form, id):
        """Called before pre-filling the form with data from the model"""
        user = db.session.query(User).get(id)
        form.password.data = user.password  # You can set default data for the password field
        return super(UserModelView, self)._on_form_prefill(form, id)
