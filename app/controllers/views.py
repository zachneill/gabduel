from flask import Blueprint, render_template

from app.logic.posts import getPosts

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    """Render the home page"""
    posts = getPosts()
    return render_template("home.html", posts=posts)


@views.route('/about')
def about():
    """Render the about page"""
    return render_template("about.html")


@views.route('/404')
def page_not_found():
    """Render the 404 page"""
    return render_template("extra/404.html"), 404


@views.route('/500')
def internal_server_error():
    """Render the 500 page"""
    return render_template("extra/500.html"), 500


@views.route('/405')
def method_not_allowed():
    """Render the 405 page"""
    return render_template("extra/405.html"), 405
