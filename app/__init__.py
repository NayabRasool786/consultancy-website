#from flask_markdown import Markdown
# Import the main Flask class and other necessary libraries.
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import MetaData



# --- NEW: Define a naming convention ---
# This ensures all constraints are named, preventing errors with SQLite.
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# --- Initialize Extensions ---
# Pass the naming convention to SQLAlchemy
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
# --- ADD THIS LINE ---
login_manager.login_message_category = 'danger'



# --- Application Factory Function ---
def create_app(config_class=Config):
    """
    Creates and configures an instance of the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    # --- NEW: Initialize Markdown with the app ---
    #Markdown(app)
    # --- Initialize Flask Extensions with the App ---
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # --- Register Blueprints ---
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # --- User Loader Function ---
    # This needs to be inside the factory so it has access to the User model
    # AFTER the models have been defined and are part of the app context.
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app