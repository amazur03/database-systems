from flask_admin.contrib.sqla import ModelView
from models import db, User
from flask_admin.form.widgets import Select2Widget
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import PasswordField
from wtforms import validators
from flask_login import current_user
from werkzeug.security import generate_password_hash

class UserModelView(ModelView):
    """Admin view for the User model"""
    column_list = ('id', 'username', 'name', 'surname', 'email', 'role')
    form_columns = ('username', 'password', 'role', 'name', 'surname', 'email')
    form_extra_fields = {
        'password': PasswordField('Password')
    }
    column_searchable_list = ['username', 'email', 'name', 'surname']
    column_sortable_list = ['id', 'username', 'name', 'email', 'role', 'surname']
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

    form_choices = {
         'role': [
            ('admin', 'Admin'),
            ('controller', 'Controller'),
            ('warehouseman', 'Warehouseman')
        ]
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            if not is_created and not form.password.data.startswith("pbkdf2:sha256"):  
                model.password = generate_password_hash(form.password.data)
            elif is_created:
                model.password = generate_password_hash(form.password.data)
        super().on_model_change(form, model, is_created)

    def _on_form_prefill(self, form, id):
        user = db.session.query(User).get(id)
        form.password.data = user.password
        return super(UserModelView, self)._on_form_prefill(form, id)


    def create_model(self, form):
        # Ensure password is provided during creation
        if not form.password.data:
            form.password.errors.append("Password is required for new users.")
            return False
        model = self.model()
        form.populate_obj(model)
        # Hash the password before saving
        model.password = generate_password_hash(form.password.data)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()
        return model

    def update_model(self, form, model):
        # Check if password is being updated
        if form.password.data and not form.password.data.startswith("pbkdf2:sha256"):
            # Hash the new password if provided
            model.password = generate_password_hash(form.password.data)
        form.populate_obj(model)
        self.session.add(model)
        self._on_model_change(form, model, False)
        self.session.commit()
        return model
    
    def is_accessible(self):
        # Check if the current user is authenticated and has 'admin' role
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for
        # Redirect unauthenticated or unauthorized users to the login page
        return redirect(url_for('login'))