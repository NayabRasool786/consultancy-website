# Import the Blueprint class from Flask.
from functools import wraps
from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, logout_user, current_user
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import User

# Create a Blueprint instance for authentication-related routes.
# 'auth' is the name of the blueprint.
bp = Blueprint('auth', __name__)

# We will add login, logout, and register routes here in a later step.

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

# --- NEW LOGIN ROUTE ---
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    # If the user is already logged in, redirect them to the home page.
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Find the user by their email address.
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check if the user exists and the password is correct.
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))
            
        # If credentials are valid, log the user in.
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome back, {user.username}!', 'success')
        
        # Redirect to the page the user was trying to access, or to the home page.
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
        return redirect(next_page)
        
    return render_template('login.html', title='Sign In', form=form)

# --- NEW LOGOUT ROUTE ---
@bp.route('/logout')
def logout():
    """Handle user logout."""
    logout_user()
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a new user instance
        user = User(username=form.username.data, email=form.email.data)
        # Set the password using our secure method
        user.set_password(form.password.data)
        # Add the user to the database
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        # Redirect to the login page after successful registration
        return redirect(url_for('auth.login')) # We will create login route next
    return render_template('register.html', title='Register', form=form)

