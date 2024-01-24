from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required

from app.logic.accounts import createUser, getUserByEmail, getUserByUsername, checkPassword, getUserById, getUsers, \
    makeAdmin
from app.logic.posts import createPost
from app.models.forms.LoginForm import LoginForm
from app.models.forms.PostForm import PostForm
from app.models.forms.SignupForm import SignupForm
from app.models.forms.AdminForm import AdminForm
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
    form = LoginForm()
    if form.validate_on_submit():
        user = getUserByEmail(form.email.data)
        if user:
            if checkPassword(user.password, form.password.data):
                flash(f'{user.firstName} logged in!', 'success')
                login_user(user, remember=form.rememberMe.data)
                return redirect('/home')
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
        return redirect('/home')
    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.confirmPassword.data:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for("auth.signup"))
        userEmail = getUserByEmail(form.email.data)
        userUsername = getUserByUsername(form.username.data)
        if userEmail or userUsername:
            flash('Email or username already exists!', 'danger')
            return redirect(url_for("auth.signup"))
        else:
            user = createUser({"email": form.email.data, "firstName": form.firstName.data,
                               "lastName": form.lastName.data, "username": form.username.data,
                               "password": form.password.data, "isAdmin": False})
            login_user(user, remember=form.rememberMe.data)
            flash(f'Account created for {form.firstName.data}!', 'success')
            return render_template("home.html", user=current_user)

    return render_template("signup.html", form=form, user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out!', 'success')
    return redirect('/login')


@auth.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        createPost({"content": form.content.data, "title": form.title.data, "author": current_user.id})
        flash('Post created!', 'success')
        return redirect('/home')
    return render_template("create.html", form=form, user=current_user)


@auth.route('/admin', methods=["GET", "POST"])
@login_required
def admin():
    form = AdminForm()
    if form.validate_on_submit():
        user = makeAdmin(current_user.id)
        flash(f'{user.firstName} is now an admin!', 'success')
        return redirect('/admin')
    user = getUserById(current_user.id)
    if not user.isAdmin:
        flash("You are not an admin.", category="warning")
        allUsers = None
    else:
        allUsers = getUsers()
    return render_template("admin.html", form=form, current_user=current_user, user=user, allUsers=allUsers)
