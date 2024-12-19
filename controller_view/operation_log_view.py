from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class OperationLogModelView(ModelView):
    """Admin view for the OperationLog model."""

    can_create = False
    column_list = (
        'id', 'operation_type', 'user.username', 'timestamp', 'details'
    )
    column_filters = ['operation_type', 'timestamp', 'user.username']
    column_searchable_list = ['operation_type', 'details']
    column_sortable_list = ['timestamp']

    column_labels = {
        'id': 'ID',
        'operation_type': 'Operation Type',
        'user.username': 'User',
        'timestamp': 'Timestamp',
        'details': 'Details',
    }

    column_formatters = {
        'timestamp': lambda view, context, model, name: model.timestamp.strftime('%Y-%m-%d %H:%M:%S') if model.timestamp else 'N/A',
        'user.username': lambda view, context, model, name: model.user.username if model.user else 'N/A',
    }

    form_excluded_columns = ['timestamp']  # Automatyczne ustawianie czasu

    def is_action_allowed(self, name):
        """Disable creation of new log entries."""
        if name == 'create':
            return False
        return super().is_action_allowed(name)
