# Import necessary classes from Flask-WTF and WTForms.
from flask_wtf import FlaskForm
# Import the FileField and validators for it
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Optional


# Import the User model to check for existing users
from app.models import User

# Define the ContactForm class, inheriting from FlaskForm.
class ContactForm(FlaskForm):
    """
    A form for users to send messages to the site admin.
    """
    # Define the 'name' field: a text input.
    # 'DataRequired' validator ensures the field is not submitted empty.
    name = StringField('Full Name', validators=[DataRequired()])
    
    # Define the 'email' field.
    # 'Email' validator checks if the input has a valid email format.
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    
    # Define the 'service' field: a dropdown menu.
    # 'choices' provides the options for the dropdown.
    service = SelectField('Service of Interest', choices=[
        ('general', 'General Inquiry'),
        ('strategy', 'Business Strategy'),
        ('it', 'IT Consulting'),
        ('finance', 'Financial Advisory')
    ])
    
    # Define the 'message' field: a larger text area.
    message = TextAreaField('Message', validators=[DataRequired()])
    
    # Define the 'submit' button.
    submit = SubmitField('Send Message')




class RegistrationForm(FlaskForm):
    """Form for users to create a new account."""
    username = StringField('Username', validators=[DataRequired(), Length(max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Custom validator to check if the username is already taken."""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_email(self, email):
        """Custom validator to check if the email is already registered."""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is already registered.')
        

class LoginForm(FlaskForm):
    """Form for users to log in."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class PostForm(FlaskForm):
    """Form for creating and editing blog posts."""
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=140)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10)], render_kw={'rows': 10})
    
    # --- NEW FIELDS FOR IMAGE ---
    # Field for pasting an image URL from the web. 'Optional' means it can be empty.
    image_url = StringField('Image URL (optional)', validators=[Optional(), Length(max=500)])
    
    # Field for uploading an image from the local machine.
    # 'FileAllowed' restricts the upload to specific file types.
    image_upload = FileField('Upload Image (optional)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    
    submit = SubmitField('Submit Post')


# --- NEW JOB FORM ---
class JobForm(FlaskForm):
    """Form for admins to create or edit a job posting."""
    title = StringField('Job Title', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    job_type = StringField('Job Type (e.g., Full-time)', validators=[DataRequired()])
    description = TextAreaField('Job Description', validators=[DataRequired()])
    submit = SubmitField('Submit Job Posting')