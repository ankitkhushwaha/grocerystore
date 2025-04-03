from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from .config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt



db = SQLAlchemy()
# migrate = Migrate()

def create_app():
    app = Flask(__name__)
    login_manager = LoginManager()
    app.config.from_object(Config)
    app.app_context().push()
    bcrypt = Bcrypt(app)
    
    db.init_app(app)
    db.create_all()
    login_manager.__init__(app)
    # migrate.init_app(app, db)  # Initialize Flask-Migrate with the app and db

    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Import and register the routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
