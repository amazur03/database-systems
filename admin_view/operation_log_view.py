from flask_admin.contrib.sqla import ModelView
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import SelectField, validators
from flask_login import current_user

class OperationLogModelView(ModelView):
    """Admin view for the Operation Log"""
    column_list = ('operation_type', 'user.username', 'timestamp', 'details')
    column_searchable_list = ['operation_type', 'user.username', 'details']
    column_filters = ['operation_type', 'timestamp']
    can_create = False
    can_edit = False
    can_delete = False
    column_default_sort = ('timestamp', True)

    def is_accessible(self):
        # Check if the current user is authenticated and has 'admin' role
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for
        # Redirect unauthenticated or unauthorized users to the login page
        return redirect(url_for('login'))