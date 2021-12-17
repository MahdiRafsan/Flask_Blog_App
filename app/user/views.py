import os
import uuid
from flask import render_template, redirect, url_for, flash, request, current_app, Blueprint
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
from .forms import EditProfileForm, ResetRequestForm, PasswordResetForm
from .func import send_email

#from app.posts.forms import CommentForm
from ..post.forms import CommentForm

# from app.models import User, Post
from ..models import User, Post

# from app import app, db, mail
from .. import db

user = Blueprint("user", __name__)

@user.route("/account/<username>", methods = ["GET", "POST"])
@login_required
def account(username):
    """
    allow user to update their info and image
    :param username: username of the current user
    :return: None 
    """
    form = EditProfileForm()
    if form.validate_on_submit():
        
        # save image with a unique identifier
        if form.image.data:
            secure_fn = secure_filename(form.image.data.filename)
            pic_name = uuid.uuid4().hex[:10] + os.path.splitext(secure_fn)[1]
            pic_path = os.path.join(current_app.root_path, "static/profile_pics", pic_name)

            image = Image.open(form.image.data)
            i = image.resize((150, 150))
            i.save(pic_path)
            
            current_user.image = pic_name
        else:
            image = url_for("static", filename=f"profile_pics/{current_user.image}")
        
        # update username, email, bio and password
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about = form.bio.data
        if form.new_password.data:
            current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash("Your account has successfully been updated.", category="success")
        return redirect(url_for("user.account", username=current_user.username))
    
    # populate username, email and bio fields
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.about
    
    user = User.query.filter_by(username=username).first()
    image = url_for("static", filename=f"profile_pics/{current_user.image}")
    return render_template("account.html", user=user, image=image, form=form)


@user.route("/post-by/<username>")
@login_required
def post_by_user(username):
    """
    display all posts from a certain user with latest posts first
    :param username: user whose posts are to be displayed
    :return: None
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("No user with that username found.", category="danger")
        return redirect(url_for("main.home"))

    # paginate 
    page_num = request.args.get("page", default=1, type=int)
    posts = Post.query.filter_by(post_author=user.id).order_by(Post.date.desc()).paginate(per_page=5, page=page_num, error_out=True)
    form=CommentForm()
    return render_template("user_posts.html", user=current_user, form=form, posts=posts, username=username)

@user.route("/reset-request", methods = ["GET", "POST"])
def request_token():
    """
    take user input for email and send the token
    :return: None 
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash("Please check your email for instructions to reset your password", category="info")
        return redirect(url_for("auth.login"))
    
    return render_template("request_token.html", form=form)

@user.route("/reset-password/<token>", methods = ["GET", "POST"])
def reset_password(token):
    """
    reset the password of the user with the token
    :param token: token recieved from the email
    :return: None
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_token(token)
    if not user:
        flash("The token is either invalid or has expired.", category="warning")
        return redirect(url_for("user.request_token"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash("Your password has been successfully updated.", category="success")
        return redirect(url_for("auth.login"))
    return render_template("reset_password.html", form=form)
