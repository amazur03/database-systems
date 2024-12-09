from flask_admin.contrib.sqla import ModelView
from models import Role

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



