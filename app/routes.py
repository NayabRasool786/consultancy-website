import os
import secrets
from PIL import Image
# Import the Blueprint and render_template functions from Flask.
from flask import Blueprint, render_template, flash, redirect, url_for, abort, request, current_app
# Import login_required decorator
from flask_login import login_required, current_user
from app import db
# Import ContactForm and now PostForm
from app.forms import ContactForm, PostForm, JobForm
# Import Post model
from app.models import Post, User, Job   # Make sure User is imported
# Import the new decorator and form
from app.auth import admin_required

# Create a Blueprint instance.
bp = Blueprint('main', __name__)

# --- Main Page Routes ---

@bp.route('/')
@bp.route('/home')
def index():
    """Renders the home page with recent posts."""
    # Fetch the 3 most recent posts
    recent_posts = Post.query.order_by(Post.timestamp.desc()).limit(3).all()
    return render_template('home.html', title='Home', posts=recent_posts)

@bp.route('/about')
def about():
    """Renders the About Us page."""
    return render_template('about.html', title='About Us')

@bp.route('/services')
def services():
    """Renders the Our Services page."""
    return render_template('services.html', title='Our Services')

# Add placeholders for other pages for now
@bp.route('/for-clients')
@login_required  # <-- ADD THIS DECORATOR
def for_clients():
    """Renders the For Clients page."""
    return render_template('for_clients.html', title='For Clients')

@bp.route('/for-hire')
@login_required  # <-- ADD THIS DECORATOR
def for_hire():
    """Renders the For Hire page."""
    return render_template('for_hire.html', title='For Hire')

@bp.route('/careers')
def careers():
    """Renders the Careers page with job openings from the database."""
    # Fetch all jobs from the database
    jobs = Job.query.order_by(Job.id).all()
    return render_template('careers.html', title='Careers', jobs=jobs)

# --- NEW ROUTE TO VIEW A SINGLE JOB OPENING ---
@bp.route('/career/<int:job_id>')
@login_required  # <-- ADD THIS DECORATOR
def job_opening(job_id):
    """Renders a single job opening page."""
    job = Job.query.get_or_404(job_id)
    return render_template('job_opening.html', title=job.title, job=job)


@bp.route('/contact', methods=['GET', 'POST']) # Allow both GET and POST requests
@login_required  # <-- ADD THIS DECORATOR
def contact():
    """Renders the Contact Us page and handles form submission."""
    form = ContactForm() # Create an instance of the form
    
    # The validate_on_submit() method checks if it's a POST request and if the data is valid.
    if form.validate_on_submit():
        # If the form is valid, we can process the data.
        # For now, we'll just flash a success message.
        # In a real app, you would send an email here.
        name = form.name.data
        flash(f'Thank you for your message, {name}! We will get back to you shortly.', 'success')
        
        # Redirect to the same contact page to prevent form re-submission on refresh.
        return redirect(url_for('main.contact'))
        
    # If it's a GET request or the form is invalid, render the template with the form object.
    return render_template('contact.html', title='Contact Us', form=form)


# --- HELPER FUNCTION TO SAVE UPLOADED IMAGE ---
def save_picture(form_picture):
    # Generate a random hex to be the new filename to avoid collisions
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)

    # Resize the image to a max size (e.g., 1200px width) to save space
    output_size = (1200, 1200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        image_filename = None
        # Logic to decide which image source to use
        if form.image_upload.data:
            image_filename = save_picture(form.image_upload.data)
        elif form.image_url.data:
            image_filename = form.image_url.data

        post = Post(
            title=form.title.data, 
            content=form.content.data, 
            author=current_user,
            image_file=image_filename  # Save the image filename/URL
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.blog'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


# --- UPDATED BLOG ROUTE TO DISPLAY ALL POSTS ---
@bp.route('/blog')
def blog():
    """Renders the Blog page with all posts."""
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog.html', title='Blog', posts=posts)

# --- NEW ROUTE TO VIEW A SINGLE POST ---
@bp.route('/post/<int:post_id>')
def post(post_id):
    """Renders a single blog post page."""
    # get_or_404 will automatically return a 404 error if the post ID is not found
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


# --- NEW ROUTE TO UPDATE A POST ---
@bp.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and not current_user.is_admin:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        # Handle updating the image
        if form.image_upload.data:
            post.image_file = save_picture(form.image_upload.data)
        elif form.image_url.data:
            post.image_file = form.image_url.data

        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        # Pre-fill the URL field if the image is from the web
        if post.image_file and post.image_file.startswith('http'):
            form.image_url.data = post.image_file
            
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


# --- NEW ROUTE TO DELETE A POST ---
@bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Handles deleting a blog post."""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and not current_user.is_admin:
        abort(403) # Security check
    
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('main.blog'))


# --- ADMIN-ONLY JOB MANAGEMENT ROUTES ---

@bp.route('/create_job', methods=['GET', 'POST'])
@login_required
@admin_required
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, location=form.location.data, job_type=form.job_type.data, description=form.description.data)
        db.session.add(job)
        db.session.commit()
        flash('The job posting has been created.', 'success')
        return redirect(url_for('main.careers'))
    return render_template('create_job.html', title='Create Job Posting', form=form)

@bp.route('/job/<int:job_id>/update', methods=['GET', 'POST'])
@login_required
@admin_required
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    form = JobForm()
    if form.validate_on_submit():
        job.title = form.title.data
        job.location = form.location.data
        job.job_type = form.job_type.data
        job.description = form.description.data
        db.session.commit()
        flash('The job posting has been updated.', 'success')
        return redirect(url_for('main.job_opening', job_id=job.id))
    elif request.method == 'GET':
        form.title.data = job.title
        form.location.data = job.location
        form.job_type.data = job.job_type
        form.description.data = job.description
    return render_template('create_job.html', title='Update Job Posting', form=form)

@bp.route('/job/<int:job_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('The job posting has been deleted.', 'success')
    return redirect(url_for('main.careers'))