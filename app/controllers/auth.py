from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash

from app.logic.accounts import createUser, getUserByEmail, getUserByUsername, checkPassword
from app.models.LoginForm import LoginForm
from app.models.SignupForm import SignupForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/welcome')
    form = LoginForm()
    if form.validate_on_submit():
        user = getUserByEmail(form.email.data)
        if user:
            if checkPassword(user.password, form.password.data):
                flash(f'{user.firstName} logged in!', 'success')
                login_user(user, remember=True)
                return redirect('/welcome')
            else:
                flash(f'Incorrect password for {form.email.data}', 'danger')
                return redirect('/login')
        else:
            flash(f'No account exists for {form.email.data}', 'danger')
            return redirect('/login')
    return render_template("login.html", form=form, user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect('/welcome')
    form = SignupForm()
    if form.validate_on_submit():
        userEmail = getUserByEmail(form.email.data)
        userUsername = getUserByUsername(form.username.data)
        if userEmail or userUsername:
            flash(f'Email or username already exists!', 'danger')
            return redirect(url_for("auth.signup"))
        else:
            user = createUser({"email": form.email.data, "firstName": form.firstName.data,
                        "lastName": form.lastName.data, "username": form.username.data,
                        "password": form.password.data})
            login_user(user, remember=True)
            flash(f'Account created for {form.firstName.data}!', 'success')
            return render_template("welcome.html", user=current_user)

    return render_template("signup.html", form=form, user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'Successfully logged out!', 'success')
    return redirect('/login')
