from flask_admin.contrib.sqla import ModelView
from models import db, Unit

class UnitModelView(ModelView):
    """Admin view for the Unit model."""
    column_list = ('id', 'name', 'percentage_of_the_stock')
    form_columns = ('id', 'name', 'percentage_of_the_stock')
    column_filters = ['name']
    column_searchable_list = ['name']
    column_formatters = {
        'percentage_of_the_stock': lambda view, context, model, name: 
            f"{model.percentage_of_the_stock:.2f}%" if model.percentage_of_the_stock is not None else 'N/A'
    }
