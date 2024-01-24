from flask import Blueprint, render_template, redirect, flash, request
from flask_login import login_required, current_user

from app.logic.accounts import getUserById, getUsers, makeAdmin
from app.logic.posts import getPosts

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
@login_required
def home():
    posts = getPosts()
    return render_template("home.html", user=current_user, posts=posts)


@views.route('/about')
def about():
    return render_template("about.html", user=current_user)