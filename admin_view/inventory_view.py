from flask_admin.contrib.sqla import ModelView
from models import db, WarehouseMove, User
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import SelectField, validators

class InventoryModelView(ModelView):
    column_list = ('id', 'date')
    form_columns = ('id', 'date')
    column_filters = ['id', 'date']
    column_searchable_list = ['id', 'date']
    column_sortable_list = ['id', 'date']