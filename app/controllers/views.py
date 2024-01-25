from flask import Blueprint, render_template
from flask_login import current_user

from app.logic.posts import getPosts

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    """Render the home page"""
    try:
        posts = getPosts()
    except Exception as e:
        posts = None
        print("Failed to get posts with error", e)
    return render_template("home.html", posts=posts)


@views.route('/about')
def about():
    """Render the about page"""
    return render_template("about.html", user=current_user)
