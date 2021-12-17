from flask import render_template, redirect, url_for, flash, request, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from .forms import SignUpForm, LoginForm
from .. import db

auth = Blueprint("auth", __name__)

@auth.route("/sign-up", methods = ["GET", "POST"])
def sign_up():
    """
    displays the sign-up page and registers a new user
    validates the username is not taken and hashes passwords for security
    :return: None
    """
    form = SignUpForm()

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, 
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully for {form.username.data}! You are now able to login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template("sign-up.html", form = form) 

@auth.route("/login", methods = ["GET", "POST"])
def login():
    """
    displays the login page and log in a registered user
    :return: None
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                flash("Logged in succesfully!", category="success")
                login_user(user, remember=form.remember.data)
                next = request.args.get("next")
                return redirect(next) if next else redirect(url_for("main.home"))
            else:
                flash("Incorrect password! Please try again.", category="danger")
        else:
            flash("Email does not exist! Please check your email.", category="danger")

    return render_template("login.html", form = form)

@auth.route("/logout")
@login_required
def logout():
    """
    logs the user out 
    :return: None
    """
    logout_user()
    return redirect(url_for("auth.login"))
