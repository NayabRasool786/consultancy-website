# Import the database instance and the LoginManager's UserMixin.
from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# THE @login_manager.user_loader FUNCTION HAS BEEN REMOVED FROM THIS FILE.

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256)) # Increased length for stronger hashes

    # We replaced backref='author' with back_populates='author'
    posts = db.relationship('Post', back_populates='author', lazy='dynamic')
    # Add a boolean field to mark users as administrators.
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def set_password(self, password):
        """Creates a hashed password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the submitted password matches the hashed one."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# We'll add the Post model for the blog here later.
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # This explicitly creates the 'post.author' attribute
    author = db.relationship('User', back_populates='posts')
    # This will store the URL or the filename of the post's image.
    image_file = db.Column(db.String(120), nullable=False, default='https://img.freepik.com/free-photo/technology-communication-icons-symbols-concept_53876-120314.jpg')

    def __repr__(self):
        return f'<Post {self.title}>'
    

# --- NEW JOB MODEL ---
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(50), nullable=False, default='Full-time')
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Job {self.title}>'