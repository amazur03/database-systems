from flask_admin.contrib.sqla import ModelView
from models import db, WarehouseMove, User
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import SelectField, validators

class ControllerInventoryModelView(ModelView):
    column_list = ('id', 'description', 'date')
    form_columns = ('description', 'date')
    column_filters = ['date']
    column_searchable_list = ['date']
    column_sortable_list = ['date']