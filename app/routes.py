from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, current_user, logout_user
from app import app
from app.forms import LoginForm, RegisterForm
from app.models import Post, User
from werkzeug.urls import url_parse
from app import db


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = Post.query.filter_by(author=current_user).all()
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user=user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if next_page is not None and url_parse(next_page).netloc == '':
            flash('Welcome')
            return redirect(next_page or url_for('index'))

        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('Registered')
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>/')
@login_required
def user_profile(username):
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Post.query.filter_by(author=user).all()
    return render_template('user_profile.html', title='Profile', posts=posts)
