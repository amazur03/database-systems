from flask_admin.contrib.sqla import ModelView
from models import db, User
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import PasswordField
from wtforms import validators

class UserModelView(ModelView):
    """Admin view for the User model"""
    column_list = ('id', 'username', 'name', 'surname', 'email', 'role')
    form_columns = ('id', 'username', 'password', 'role', 'name', 'surname', 'email')
    form_extra_fields = {
        'password': PasswordField('Password')
    }
    column_searchable_list = ['username', 'email', 'name', 'surname']
    column_sortable_list = ['username', 'name', 'email']
    column_filters = ['role', 'email']
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
