from flask_admin.contrib.sqla import ModelView
from models import db, User, Role
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import PasswordField
from wtforms import validators

class UserModelView(ModelView):
    """Admin view for the User model"""
    column_list = ('id', 'username', 'name', 'surname', 'email', 'role.role_name')
    form_columns = ('id', 'username', 'password', 'role', 'name', 'surname', 'email')
    form_extra_fields = {
        'role': QuerySelectField(
            'Role',
            query_factory=lambda: db.session.query(Role).all(),
            widget=Select2Widget(),
            get_label=lambda role: role.role_name
        ),
        'password': PasswordField('Password')
    }
    column_searchable_list = ['username', 'email', 'name', 'surname']
    column_sortable_list = ['username', 'name', 'email']
    column_formatters = {
        'role.role_name': lambda view, context, model, name: model.role.role_name if model.role else 'N/A'
    }
    column_filters = ['role.role_name', 'email']
    form_labels = {
        'username': 'Username',
        'name': 'First Name',
        'surname': 'Last Name',
        'email': 'Email Address',
        'role': 'Role',
        'password': 'Password'
    }
    form_widget_args = {
        'password': {
            'type': 'password'
        }
    }

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password = form.password.data
        return super(UserModelView, self).on_model_change(form, model, is_created)

    def _on_form_prefill(self, form, id):
        user = db.session.query(User).get(id)
        form.password.data = user.password
        return super(UserModelView, self)._on_form_prefill(form, id)