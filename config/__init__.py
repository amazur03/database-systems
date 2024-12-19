from flask import Flask, redirect, url_for, request, render_template
from flask_migrate import Migrate
from models import db
from flask_admin import Admin, AdminIndexView, expose
from models import Unit, Product, User, WarehouseMove, WarehouseMoveProduct, Inventory, InventoryProduct, OperationLog
from admin_view import ProductModelView, UnitModelView, UserModelView, WarehouseMoveModelView, WarehouseMoveProductModelView, UserModelView, InventoryModelView, InventoryProductModelView, OperationLogModelView
from controller_view import ControllerInventoryProductModelView, ControllerInventoryModelView, ControllerWarehouseMoveModelView, ControllerWarehouseMoveProductModelView, OperationLogModelView, ControllerProductModelView
from warehouseman_view import WarehousemanWarehouseMoveModelView, WarehousemanWarehouseMoveProductModelView, WarehousemanProductModelView, OperationLogModelView
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import logging
from flask_admin.menu import MenuLink
from werkzeug.security import generate_password_hash, check_password_hash



logging.basicConfig(level=logging.INFO)

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'login'

# Initialize the database object globally
migrate = Migrate()

def register_extensions(app):
    # Initialize the database with the app
    db.init_app(app)
    app.logger.info('Database initialized')

    # Initialize Flask-Migrate for database migrations
    migrate.init_app(app, db)
    app.logger.info('Migration initialized')

    # Initialize Flask-Login
    login_manager.init_app(app)
    app.logger.info('Login manager initialized')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Flask-Admin secure index view
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        return super(MyAdminIndexView, self).index()
    


def configure_admin_panel(app):
    admin = Admin(app, name='Admin Panel', endpoint='admin', url='/admin')  # The 'Management Panel' will be the name displayed in the admin panel
    admin.add_link(MenuLink(name='Logout', url='/logout'))
    admin.add_view(UserModelView(User, db.session, endpoint='admin_user', name='Users', category='Users Menagment'))
    admin.add_view(ProductModelView(Product, db.session, endpoint='admin_product', name='Product', category='Product Menagment'))
    admin.add_view(UnitModelView(Unit, db.session, endpoint='admin_unit', name='Unit', category='Product Menagment'))
    admin.add_view(WarehouseMoveModelView(WarehouseMove, db.session, endpoint='admin_warehous_move', name='Warehouse Moves', category='Warehouse Menagment'))
    admin.add_view(WarehouseMoveProductModelView(WarehouseMoveProduct, db.session, endpoint='admin_warehous_move_prod', name='Warehous Moves Products', category='Warehouse Menagment'))
    admin.add_view(InventoryModelView(Inventory, db.session, endpoint='admin_inventory', name='Inventory', category='Inventory Menagment'))
    admin.add_view(InventoryProductModelView(InventoryProduct, db.session, endpoint='admin_inventory_product', name='Inventory Products', category='Inventory Menagment'))
    admin.add_view(OperationLogModelView(OperationLog, db.session, endpoint='admin_operation_log', name='Operation Logs', category='Logs'))

def configure_controller_panel(app):
    controller = Admin(app, name='Controller Panel', endpoint='controller', url='/controller')  # The 'Management Panel' will be the name displayed in the admin panel
    controller.add_link(MenuLink(name='Logout', url='/logout'))
    controller.add_view(ControllerProductModelView(Product, db.session, endpoint='controller_product', name='Product', category='Product Menagment'))
    controller.add_view(ControllerWarehouseMoveModelView(WarehouseMove, db.session, endpoint='controller_warehous_move', name='Warehouse Moves', category='Warehouse Menagment'))
    controller.add_view(ControllerWarehouseMoveProductModelView(WarehouseMoveProduct, db.session, endpoint='controller_warehous_move_prod', name='Warehous Moves Products', category='Warehouse Menagment'))
    controller.add_view(ControllerInventoryModelView(Inventory, db.session, endpoint='controller_admin_inventory', name='Inventory', category='Inventory Menagment'))
    controller.add_view(ControllerInventoryProductModelView(InventoryProduct, db.session, endpoint='controller_inventory_product', name='Inventory Products', category='Inventory Menagment'))
    controller.add_view(OperationLogModelView(OperationLog, db.session, endpoint='controller_operation_log', name='Operation Logs', category='Logs'))

def configure_warehouseman_panel(app):
    warehouseman = Admin(app, name='Warehouseman Panel', endpoint='warehouseman', url='/warehouseman')  # The 'Management Panel' will be the name displayed in the admin panel
    warehouseman.add_link(MenuLink(name='Logout', url='/logout'))
    warehouseman.add_view(WarehousemanWarehouseMoveModelView(WarehouseMove, db.session, endpoint='warehouseman_warehous_move', name='Warehouse Moves', category='Warehouse Menagment'))
    warehouseman.add_view(WarehousemanWarehouseMoveProductModelView(WarehouseMoveProduct, db.session, endpoint='warehouseman_warehous_move_prod', name='Warehous Moves Products', category='Warehouse Menagment'))
    warehouseman.add_view(WarehousemanProductModelView(Product, db.session, endpoint='warehouseman_product', name='Product', category='Product Menagment'))
    warehouseman.add_view(OperationLogModelView(OperationLog, db.session, endpoint='warehouseman_operation_log', name='Operation Logs', category='Logs'))


def configure_app(app):
    # Set the secret key to use for the session, change this later
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')



    # Configure the app
    configure_app(app)
    app.logger.info('App configured successfully')

    try:
        # Register extensions
        register_extensions(app)

        # Build admin panel from flask-admin
        configure_admin_panel(app)
        configure_controller_panel(app)
        configure_warehouseman_panel(app)

        # Add routes for login/logout and product addition
        add_auth_routes(app)
        #add_product_routes(app)  # To będzie nowa funkcja, którą trzeba dodać
        create_admin_user(app)

        app.logger.info('App created successfully')
        return app
    except Exception as e:
        app.logger.error(f'Error in creating app: {str(e)}')
        raise

def create_admin_user(app):
    try:
        with app.app_context():
            # Check if an admin user exists
            if not User.query.filter_by(role="admin").first():
                app.logger.info('No admin user found, creating default admin user.')
                
                # Create the default admin user with a hashed password
                admin_user = User(
                    username='admin',
                    password='admin123!',  # Haszowanie hasła
                    name="admin",
                    surname="admin",
                    email="admin@example.com",  # You can use a default email address
                    role="admin"
                )
                
                # Add the admin user to the session and commit to the database
                db.session.add(admin_user)
                db.session.commit()
                
                app.logger.info('Default admin user created.')
    except Exception as e:
        app.logger.error(f"Error creating default admin user: {str(e)}")
        pass
def add_auth_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            # Wyszukiwanie użytkownika w bazie danych
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password, password):  # Weryfikacja hasła
                login_user(user)
                
                # Przekierowanie na podstawie roli użytkownika
                if user.role == 'admin':
                    return redirect(url_for('admin.index'))
                elif user.role == 'controller':
                    return redirect(url_for('controller.index'))
                elif user.role == 'warehouseman':
                    return redirect(url_for('warehouseman.index'))
                else:
                    return 'Nieznana rola użytkownika', 403
            
            # Błędne dane logowania
            return 'Invalid username or password', 401
        
        # Formularz logowania
        return render_template('login.html')

    # Logout route
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
