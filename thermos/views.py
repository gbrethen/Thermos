from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user

from thermos import app
from thermos import db
from thermos import login_manager
from thermos.forms import BookmarkForm, LoginForm
from thermos.models import User, Bookmark

# Fake Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index')
def index():
   return render_template('index.html', new_bookmarks=Bookmark.newest(5))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = Bookmark(user=current_user, url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        flash(f"stored : {description}")
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            print(f"user: {user}")
            login_user(user, form.remember_me.data)
            flash(f"Logged in successfully as {user.username}")
            return redirect(request.args.get('next') or url_for('index'))
        flash('Incorrect username or password.')
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome, {user.username}! Please login.')
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500