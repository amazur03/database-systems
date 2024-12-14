from flask_admin.contrib.sqla import ModelView
from models import db, WarehouseMove, User
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import SelectField, validators

class WarehouseMoveModelView(ModelView):
    """Admin view for the WarehouseMove model."""
    column_list = ('id', 'move_type', 'order_date', 'implementation_date', 'user.username')
    form_columns = ('move_type', 'order_date', 'implementation_date', 'user')
    column_filters = ['move_type', 'order_date', 'implementation_date', 'user.username']
    column_searchable_list = ['move_type', 'user.username']
    column_sortable_list = ['move_type', 'order_date', 'implementation_date']
    form_extra_fields = {
        'user': QuerySelectField(
            'User',
            query_factory=lambda: db.session.query(User).all(),
            widget=Select2Widget(),
            get_label=lambda user: user.username
        ),
        'move_type': SelectField(
            'Move Type',
            choices=[('IN', 'IN'), ('OUT', 'OUT')],
            validators=[validators.InputRequired()]
        ),
    }
    column_formatters = {
        'user.username': lambda view, context, model, name: model.user.username if model.user else 'N/A',
        'order_date': lambda view, context, model, name: model.order_date.strftime('%Y-%m-%d') if model.order_date else 'N/A',
        'implementation_date': lambda view, context, model, name: model.implementation_date.strftime('%Y-%m-%d') if model.implementation_date else 'N/A'
    }
    form_args = {
        'order_date': {
            'validators': [validators.InputRequired()]
        },
        'implementation_date': {
            'validators': [validators.InputRequired()]
        }
    }

    def on_model_change(self, form, model, is_created):
        return super(WarehouseMoveModelView, self).on_model_change(form, model, is_created)

    def _on_form_prefill(self, form, id):
        return super(WarehouseMoveModelView, self)._on_form_prefill(form, id)
