from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
@login_required
def home():
    # get all post when in home page
    posts = Post.query.all()
    # pass the current user and the post to the home.html
    return render_template('home.html', user=current_user, posts=posts)


@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post Created!', category='success')
            # after post is created return user to home
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)

# Add id variable to path (dynamic path).
# The id is ten passed to the function as the parameter id.
# When in the function we'll check if the id associated with
# the user is valid to delete the post


@views.route('/delete-post/<id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash('Post does not exist', category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')

    return redirect(url_for('views.home'))

# get all post from specific user


@views.route('/posts/<username>')
@login_required
def posts(username):
    # check if user exists
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=user.id).all()
    return render_template('posts.html', user=current_user, posts=posts, username=username)
