from flask_admin.contrib.sqla import ModelView
from models import db, WarehouseMove, User, OperationLog
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import SelectField, validators
from flask_login import current_user
from sqlalchemy.event import listens_for
from datetime import datetime

class ControllerWarehouseMoveModelView(ModelView):
    """Admin view for the WarehouseMove model."""
    column_list = ('id', 'move_type', 'order_date', 'implementation_date', 'user.username')
    form_columns = ('move_type', 'order_date', 'implementation_date', 'user')
    column_filters = ['move_type', 'order_date', 'implementation_date', 'user.username']
    column_searchable_list = ['move_type', 'user.username']
    column_sortable_list = ['id', 'move_type', 'order_date', 'implementation_date', 'user.username']
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

    column_labels = {
        'id': 'ID',
        'move_type': 'Move Type',
        'order_date': 'Order Date',
        'implementation_date': 'Implementation Date',
        'user.username': 'User'
    }
    
    can_create = True
    can_edit = True
    can_delete = False

    def on_model_change(self, form, model, is_created):
        return super(ControllerWarehouseMoveModelView, self).on_model_change(form, model, is_created)

    def _on_form_prefill(self, form, id):
        return super(ControllerWarehouseMoveModelView, self)._on_form_prefill(form, id)

    def is_accessible(self):
        # Check if the current user is authenticated and has 'admin' role
        return current_user.is_authenticated and current_user.role == 'controller'

    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for
        # Redirect unauthenticated or unauthorized users to the login page
        return redirect(url_for('login'))

