from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user

from app.logic.accounts import getAuthors, getUserByUsername
from app.logic.posts import getPosts, getSearchResults, getUserPosts, getSpecialPosts, getUserSupportedPostsById, \
    getUserSupportedPostsCountById
from app.models.forms.search_form import SearchForm

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
def home():
    """Render the home page"""
    # Get the posts
    posts = getPosts()
    if current_user.is_authenticated:
        supportedPostObjects = getUserSupportedPostsById(current_user.id)
        supportedPostIds = [support.postId for support in supportedPostObjects]
        supportedPosts = {support.postId: support.authorId for support in supportedPostObjects}
    else:
        supportedPostIds = []
        supportedPosts = {}
    # Paginate the posts
    page = request.args.get('page', 1, type=int)
    pages = posts.paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts, pages=pages, supportedPosts=supportedPosts,
                           supportedPostIds=supportedPostIds)


@views.route('/about')
def about():
    """Render the about page"""
    authors = getAuthors()
    return render_template("about.html", authors=authors)


@views.route('/settings')
def settings():
    """Render the settings page"""
    return render_template("settings.html")


@views.route('/profile/<username>')
def profile(username):
    """Render the profile page"""
    user = getUserByUsername(username)
    if user is None:
        flash(f"Username {username} not found in database")
        return redirect(url_for('views.page_not_found'))
    userPosts = getUserPosts(user)
    # Paginate the posts
    page = request.args.get('page', 1, type=int)
    pages = userPosts.paginate(page=page, per_page=5)
    # Get times supported
    supports = getUserSupportedPostsCountById(user.id)
    # Get supported posts
    if current_user.is_authenticated:
        supportedPostObjects = getUserSupportedPostsById(current_user.id)
        supportedPostIds = [support.postId for support in supportedPostObjects]
        supportedPosts = {support.postId: support.authorId for support in supportedPostObjects}
    else:
        supportedPostIds = []
        supportedPosts = {}

    return render_template("profile.html", user=user, userPosts=userPosts, pages=pages,
                           url=username, supports=supports, supportedPostIds=supportedPostIds,
                           supportedPosts=supportedPosts)


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
    # Get supported posts
    if current_user.is_authenticated:
        supportedPostObjects = getUserSupportedPostsById(current_user.id)
        supportedPostIds = [support.postId for support in supportedPostObjects]
        supportedPosts = {support.postId: support.authorId for support in supportedPostObjects}
    else:
        supportedPostIds = []
        supportedPosts = {}
    if form.validate_on_submit():
        return redirect(url_for('views.search', query=form.search.data))

    return render_template("search.html", posts=posts, pages=pages, form=form, query=query,
                           supportedPosts=supportedPosts, supportedPostIds=supportedPostIds)


@views.route('/special/<kind>/<query>')
def special(kind, query):
    """Render the special page"""
    posts = getSpecialPosts(kind, query)
    # Paginate the posts
    page = request.args.get('page', 1, type=int)
    pages = posts.paginate(page=page, per_page=5)
    # Get supported posts
    if current_user.is_authenticated:
        supportedPostObjects = getUserSupportedPostsById(current_user.id)
        supportedPostIds = [support.postId for support in supportedPostObjects]
        supportedPosts = {support.postId: support.authorId for support in supportedPostObjects}
    else:
        supportedPostIds = []
        supportedPosts = {}
    return render_template("special.html", posts=posts, pages=pages,
                           kind=kind, query=query, supportedPosts=supportedPosts, supportedPostIds=supportedPostIds)


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
