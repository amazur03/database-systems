from flask import Flask, redirect, url_for, request, render_template_string
from flask_migrate import Migrate
from models import db
from flask_admin import Admin, AdminIndexView, expose
from models import Unit, Product, User, WarehouseMove, WarehouseMoveProduct, Inventory, InventoryProduct
#from admin_view import ProductModelView, UnitModelView, UserModelView, WarehouseMoveModelView, WarehouseMoveProductModelView, UserModelView, InventoryModelView, InventoryProductModelView
#from controller_view import ControllerInventoryProductModelView, ControllerInventoryModelView, ControllerWarehouseMoveModelView, ControllerWarehouseMoveProductModelView
from warehouseman_view import WarehousemanWarehouseMoveModelView, WarehousemanWarehouseMoveProductModelView, WarehousemanProductModelView
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import logging

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
'''
def configure_flask_admin(app):
    admin = Admin(app, name='Admin Panel')  # The 'Management Panel' will be the name displayed in the admin panel
    admin.add_view(UserModelView(User, db.session, endpoint='admin_user', name='Users', category='Users Menagment'))
    admin.add_view(ProductModelView(Product, db.session, endpoint='admin_product', name='Product', category='Product Menagment'))
    admin.add_view(UnitModelView(Unit, db.session, endpoint='admin_unit', name='Unit', category='Product Menagment'))
    admin.add_view(WarehouseMoveModelView(WarehouseMove, db.session, endpoint='admin_warehous_move', name='Warehouse Moves', category='Warehouse Menagment'))
    admin.add_view(WarehouseMoveProductModelView(WarehouseMoveProduct, db.session, endpoint='admin_warehous_move_prod', name='Warehous Moves Products', category='Warehouse Menagment'))
    admin.add_view(InventoryModelView(Inventory, db.session, endpoint='admin_inventory', name='Inventory', category='Inventory Menagment'))
    admin.add_view(InventoryProductModelView(InventoryProduct, db.session, endpoint='admin_inventory_product', name='Inventory Products', category='Inventory Menagment'))
    admin.add_view(OperationLogModelView(OperationLog, db.session, name='Logi Operacji', category='Logowanie'))
'''
'''
def configure_flask_admin(app):
    controller = Admin(app, name='Controller Panel')  # The 'Management Panel' will be the name displayed in the admin panel
    controller.add_view(ControllerWarehouseMoveModelView(WarehouseMove, db.session, endpoint='controller_warehous_move', name='Warehouse Moves', category='Warehouse Menagment'))
    controller.add_view(ControllerWarehouseMoveProductModelView(WarehouseMoveProduct, db.session, endpoint='controller_warehous_move_prod', name='Warehous Moves Products', category='Warehouse Menagment'))
    controller.add_view(ControllerInventoryModelView(Inventory, db.session, endpoint='controller_admin_inventory', name='Inventory', category='Inventory Menagment'))
    controller.add_view(ControllerInventoryProductModelView(InventoryProduct, db.session, endpoint='controller_inventory_product', name='Inventory Products', category='Inventory Menagment'))
    #controller.add_view(OperationLogModelView(OperationLog, db.session, name='Logi Operacji', category='Logowanie'))
'''
def configure_flask_admin(app):
    warehouseman = Admin(app, name='Warehouseman Panel')  # The 'Management Panel' will be the name displayed in the admin panel
    warehouseman.add_view(WarehousemanWarehouseMoveModelView(WarehouseMove, db.session, endpoint='warehouseman_warehous_move', name='Warehouse Moves', category='Warehouse Menagment'))
    warehouseman.add_view(WarehousemanWarehouseMoveProductModelView(WarehouseMoveProduct, db.session, endpoint='warehouseman_warehous_move_prod', name='Warehous Moves Products', category='Warehouse Menagment'))
    warehouseman.add_view(WarehousemanProductModelView(Product, db.session, endpoint='warehouseman_product', name='Product', category='Product Menagment'))
    #warehouseman.add_view(OperationLogModelView(OperationLog, db.session, name='Logi Operacji', category='Logowanie'))


def configure_app(app):
    # Set the secret key to use for the session, change this later
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

def create_app():
    app = Flask(__name__)

    # Configure the app
    configure_app(app)
    app.logger.info('App configured successfully')

    try:
        # Register extensions
        register_extensions(app)

        # Build admin panel from flask-admin
        configure_flask_admin(app)

        # Add routes for login/logout and product addition
        #add_auth_routes(app)
        #add_product_routes(app)  # To będzie nowa funkcja, którą trzeba dodać

        app.logger.info('App created successfully')
        return app
    except Exception as e:
        app.logger.error(f'Error in creating app: {str(e)}')
        raise

def add_auth_routes(app):
    # Simple login page
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username, password=password).first()  # Note: Replace with hashed password checking
            if user:
                login_user(user)
                return redirect(url_for('admin.index'))
            else:
                return 'Invalid username or password', 401

        return render_template_string('''
            <form method="POST">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
        ''')

    # Logout route
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
