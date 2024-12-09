from flask_admin.contrib.sqla import ModelView
from models import db, Product, Unit
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField

class ProductModelView(ModelView):
    """Admin view for the Product model"""
    column_list = ('id', 'name', 'unit.name', 'max_stock', 'min_stock', 'current_stock')
    form_columns = ('id', 'name', 'unit', 'max_stock', 'min_stock', 'current_stock')
    form_extra_fields = {
        'unit': QuerySelectField(
            'Unit',
            query_factory=lambda: db.session.query(Unit).all(),
            widget=Select2Widget(),
            get_label=lambda unit: f"{unit.name} ({unit.percentage_of_the_stock:.2f}%)"
        )
    }
    column_searchable_list = ['name']
    column_sortable_list = ['name', 'current_stock']
    column_formatters = {
        'unit.name': lambda view, context, model, name: f"{model.unit.name} ({model.unit.percentage_of_the_stock:.2f}%)" if model.unit else 'N/A'
    }
    column_filters = ['unit.name', 'current_stock']
    form_labels = {
        'name': 'Product Name',
        'unit': 'Unit',
        'max_stock': 'Maximum Stock',
        'min_stock': 'Minimum Stock',
        'current_stock': 'Current Stock'
    }
