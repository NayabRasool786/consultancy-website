# Import the 'os' module to interact with the operating system, used for environment variables.
import os

# Define a base directory for the project to locate files like the database.
basedir = os.path.abspath(os.path.dirname(__file__))

# Create a configuration class to hold all settings.
class Config:
    """
    Base configuration class. Contains settings common to all environments.
    """
    # SECRET_KEY is crucial for security, used for session signing and CSRF protection.
    # It's loaded from an environment variable for security reasons. Default is a simple string for development.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-hard-to-guess-string'

    # Configure the database.
    # We specify the database URI to connect to. Here, we're using SQLite.
    # The database file will be located in the project's base directory.
    # Prioritize the DATABASE_URL environment variable if it exists (for Render)
    # Otherwise, fall back to the local SQLite database.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    

    # This setting disables a Flask-SQLAlchemy feature that signals the application
    # every time a change is about to be made in the database, which is not needed.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Folder where uploaded files will be stored.
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/post_images')