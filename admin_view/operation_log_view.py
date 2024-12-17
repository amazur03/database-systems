from flask_admin.contrib.sqla import ModelView
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import SelectField, validators

class OperationLogModelView(ModelView):
    """Admin view for the Operation Log"""
    column_list = ('operation_type', 'user.username', 'timestamp', 'details')
    column_searchable_list = ['operation_type', 'user.username', 'details']
    column_filters = ['operation_type', 'timestamp']
    can_create = False
    can_edit = False
    can_delete = False
    column_default_sort = ('timestamp', True)
