from flask_admin.contrib.sqla import ModelView
from models import db, Role

class RoleModelView(ModelView):
    """Admin view for the Role model, accessible only to users with the 'admin' role."""
    column_list = ('id', 'role_name', 'permission')
    form_columns = ('id', 'role_name', 'permission')
    column_filters = ['role_name']
    column_searchable_list = ['role_name']
    column_formatters = {
        'permission': lambda view, context, model, name: 
            model.permission.decode('utf-8') if model.permission else 'None'
    }
