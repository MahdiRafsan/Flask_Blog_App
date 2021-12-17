from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flask_login import login_required, current_user
from app import db

# from forms import PostForm, CommentForm
from .forms import PostForm, CommentForm

#from app.models import Post, Like, Comment
from ..models import Post, Like, Comment

post = Blueprint("post", __name__)

@post.route("/new-post", methods = ["GET", "POST"])
@login_required
def new_post():
    """
    Create a new post for the current user
    :return: None
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, post_author=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created.", category="success")
        return redirect(url_for("main.home"))
        
    return render_template("new_post.html", form=form, title="New Post", legend="Create A New Post", button = "Post")

@post.route("/update-post/<int:post_id>", methods = ["GET", "POST"])
@login_required
def update_post(post_id):
    """
    update a post if current user is the author
    :param post_id: id of the post to be updated
    :raise 404: if post does not exist
    :raise 403: if current user is not the author
    :return: None
    """
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    
    # Abort if anyone other than author is trying to modify post 
    if post.post_author != current_user.id:
        abort(403)
    if form.validate_on_submit():
        post.title = form.title.data 
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been successfully updated.", category = "success")
        return redirect(url_for("main.home"))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("new_post.html", title="Update Post", form=form, legend="Update Post", button = "Update")

@post.route("/delete-post/<int:post_id>", methods = ["GET", "POST"])
@login_required
def delete_post(post_id):
    """
    delete a post if current user is the author
    :param post_id: id of the post to be deleted
    :raise 404: if post does not exist in database
    :raise 403: if current user is not the author
    :return: None
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been successfully deleted.", category="success")
    return redirect(url_for("main.home"))

@post.route("/new-comment/<post_id>", methods = ["POST"])
@login_required
def create_comment(post_id):
    """
    create a comment on an existing post
    :return: None
    """
    form = CommentForm()
    
    if form.validate_on_submit():
        post = Post.query.filter_by(id=post_id)    
        if post:
            comment = Comment(comment=form.comment.data, user_id=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("Post does not exist.", category="danger")
    return redirect(url_for("main.home"))

@post.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    """
    delete a comment from a post
    :param comment_id: id of the comment to be deleted
    :raise 404: if comment does not exist in database
    :raise 403: if current user is not author or owner of the post
    :return: None
    """
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user and comment.post.post_author != current_user.id:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash("Your comment has been deleted successfully!", category="success")
    return redirect(url_for("main.home"))

@post.route("/like-post/<post_id>", methods = ["GET"])
@login_required
def like_post(post_id):
    """
    create a like for a post
    :param post_id: id of the post to be liked
    :return: None 
    """
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if not like:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    else:
        db.session.delete(like)
        db.session.commit()
    return redirect(url_for("main.home"))
