from flask_admin.contrib.sqla import ModelView
from models import db, Unit
from flask_login import current_user

class UnitModelView(ModelView):
    """Admin view for the Unit model."""
    column_list = ('id', 'name', 'percentage_of_the_stock')
    form_columns = ('name', 'percentage_of_the_stock')
    column_filters = ['name']
    column_searchable_list = ['name']
    column_sortable_list = ['id', 'name', 'percentage_of_the_stock']
    column_formatters = {
        'percentage_of_the_stock': lambda view, context, model, name: 
            f"{model.percentage_of_the_stock:.2f}%" if model.percentage_of_the_stock is not None else 'N/A'
    }

    column_labels = {
        'id': 'ID',
        'name': 'Unit Name',
        'percentage_of_the_stock': 'Percentage of Stock'
    }

    def is_accessible(self):
        # Check if the current user is authenticated and has 'admin' role
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for
        # Redirect unauthenticated or unauthorized users to the login page
        return redirect(url_for('login'))