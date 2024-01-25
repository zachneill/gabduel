from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from app.logic.accounts import createUser, getUserByEmail, getUserByUsername, checkPassword, getUserById, getUsers, \
    makeAdmin
from app.logic.posts import createPost, getPostById, updatePost, deletePost
from app.models.forms.LoginForm import LoginForm
from app.models.forms.PostForm import PostForm
from app.models.forms.SignupForm import SignupForm
from app.models.forms.AdminForm import AdminForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    if current_user.is_authenticated:
        return redirect('/home')
    form = LoginForm()

    # Check if the form is valid
    if form.validate_on_submit():
        user = getUserByEmail(form.email.data)
        if user:
            # Check if the password is correct
            if checkPassword(user.password, form.password.data):
                flash(f'{user.firstName} logged in!', 'success')
                login_user(user, remember=form.rememberMe.data)
                return redirect('/home')
            else:
                flash(f'Incorrect password for {form.email.data}', 'danger')
                return redirect('/login')
        else:
            # If the user does not exist
            flash(f'No account exists for {form.email.data}', 'danger')
            return redirect('/login')
    return render_template("login.html", form=form, user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup route"""
    # Check if the user is already logged in
    if current_user.is_authenticated:
        return redirect('/home')

    form = SignupForm()
    # Check if the form is valid
    if form.validate_on_submit():
        # Check if the passwords match
        if form.password.data != form.confirmPassword.data:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for("auth.signup"))
        userEmail = getUserByEmail(form.email.data)
        userUsername = getUserByUsername(form.username.data)
        # Check if the email or username already exists
        if userEmail or userUsername:
            flash('Email or username already exists.', 'danger')
            return redirect(url_for("auth.signup"))
        else:
            # Create the user
            user = createUser({"email": form.email.data, "firstName": form.firstName.data,
                               "lastName": form.lastName.data, "username": form.username.data,
                               "password": form.password.data, "isAdmin": False})
            login_user(user, remember=form.rememberMe.data)
            flash(f'Account created for {form.firstName.data}!', 'success')
            return redirect("/home")

    return render_template("signup.html", form=form, user=current_user)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    """Logout route"""
    logout_user()
    flash('Successfully logged out!', 'success')
    return redirect('/login')


@auth.route('/post', methods=['GET', 'POST'])
@login_required
def create():
    """Create post route"""
    form = PostForm()
    # Check if the form is valid
    if form.validate_on_submit():
        # Create the post
        createPost({"content": form.content.data, "title": form.title.data, "author": current_user.id})
        flash('Post created!', 'success')
        return redirect('/home')
    return render_template("post.html", form=form, user=current_user, post=None)


@auth.route('/post/<postId>', methods=['GET', 'POST'])
@login_required
def update(postId):
    """Update post route"""
    # Check if the user is the author of the post
    post = getPostById(postId)
    if not post or post.author != current_user.id:
        flash('You are not the author of this post.', 'danger')
        return redirect('/home')
    form = PostForm(obj=post)
    # Check if the form is valid
    if form.validate_on_submit():
        # Update the post
        updatePost({"id": postId, "content": form.content.data, "title": form.title.data})
        flash('Post updated!', 'success')
        return redirect('/home')

    return render_template("post.html", form=form, user=current_user, post=post)


@auth.route('/delete', methods=['POST'])
@login_required
def delete():
    """Delete post route"""
    # Check if the user is the author of the post
    postId = int(request.form['postId'])
    post = getPostById(postId)
    # Check if the form is valid
    if post.author == current_user.id:
        # Delete the post
        deletePost({"id": postId})
    else:
        print('User is not the author')
    return redirect('/home')


@auth.route('/admin', methods=["GET", "POST"])
@login_required
def admin():
    """Admin route"""
    form = AdminForm()
    # Check if the form is valid
    if form.validate_on_submit():
        user = makeAdmin(current_user.id)
        flash(f'{user.firstName} is now an admin!', 'success')
        return redirect('/admin')

    # Check if the user is NOT an admin
    allUsers = None
    if not current_user.isAdmin:
        flash("You are not an admin.", category="warning")
    else:
        # Set up table for jinja display
        allUsers = getUsers()
    return render_template("admin.html", form=form, current_user=current_user, allUsers=allUsers)
