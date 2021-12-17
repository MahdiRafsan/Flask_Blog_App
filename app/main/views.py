from flask import render_template, request, Blueprint
from flask_login import login_required

# from app.posts.forms import CommentForm
from ..post.forms import CommentForm

# from app.models import Post
from ..models import User, Post

main = Blueprint("main", __name__)

@main.route("/", methods = ["GET", "POST"])
@main.route("/home", methods = ["GET", "POST"])
@login_required
def home():
    """
    display all posts with latest posts first
    :return: None
    """
    page_num = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(per_page=5, page=page_num, error_out=True) 
    form=CommentForm()
    return render_template("home.html", form=form, posts = posts)

@main.route("/about")
def about():
    """
    display all users/authors of the blog with their bio
    :return: None
    """
    users = User.query.all()
    page_num = request.args.get("page", default=1, type=int)
    users = User.query.paginate(per_page=5, page=page_num, error_out=True)
    return render_template("about.html", users=users)
    