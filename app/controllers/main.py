from flask import Blueprint, render_template
from flask_login import login_required, current_user
main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)


@main.route('/welcome')
@login_required
def welcome():
    return render_template("welcome.html", user=current_user)
