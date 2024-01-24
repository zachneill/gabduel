from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/welcome')
@login_required
def welcome():
    return render_template("welcome.html", user=current_user)


@views.route('/about')
def about():
    return render_template("about.html", user=current_user)
