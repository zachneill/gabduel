from flask import Blueprint, render_template, request, redirect, url_for

from app.logic.accounts import getUsers, getAuthors, getUserByUsername
from app.logic.posts import getPosts, getSearchResults, getUserPosts
from app.models.forms.SearchForm import SearchForm

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
def home():
    """Render the home page"""
    # Get the posts
    posts = getPosts()
    # Paginate the posts
    page = request.args.get('page', 1, type=int)
    pages = posts.paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts, pages=pages)


@views.route('/about')
def about():
    """Render the about page"""
    authors = getAuthors()
    return render_template("about.html", authors=authors)


@views.route('/user/<username>')
def profile(username):
    """Render the profile page"""
    user = getUserByUsername(username)
    userPosts = getUserPosts(user)
    # Paginate the posts
    page = request.args.get('page', 1, type=int)
    pages = userPosts.paginate(page=page, per_page=5)
    return render_template("profile.html", user=user, userPosts=userPosts, pages=pages)


@views.route('/search/<query>', methods=['GET', 'POST'])
def search(query):
    """Render the search page"""
    # Get the posts
    posts = getSearchResults(query)
    # Paginate the posts
    page = request.args.get('page', 1, type=int)
    pages = posts.paginate(page=page, per_page=10)
    # Add the search bar
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('views.search', query=form.search.data))

    return render_template("search.html", posts=posts, pages=pages, form=form, query=query)


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
