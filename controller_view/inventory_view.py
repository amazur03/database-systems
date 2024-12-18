from flask_admin.contrib.sqla import ModelView
from models import db, WarehouseMove, User
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import SelectField, validators
from flask_login import current_user

class ControllerInventoryModelView(ModelView):
    column_list = ('id', 'description', 'date')
    form_columns = ('description', 'date')
    column_filters = ['date']
    column_searchable_list = ['date']
    column_sortable_list = ['id', 'description', 'date']

    column_labels = {
        'id': 'ID',
        'description': 'Description',
        'date': 'Date'
    }

    can_create = True
    can_edit = True
    can_delete = False

    def is_accessible(self):
        # Check if the current user is authenticated and has 'admin' role
        return current_user.is_authenticated and current_user.role == 'controller'

    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for
        # Redirect unauthenticated or unauthorized users to the login page
        return redirect(url_for('login'))