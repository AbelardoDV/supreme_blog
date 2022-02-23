from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, current_user, logout_user
from app import app
from app.forms import EmptyForm, LoginForm, PostForm, RegisterForm
from app.models import Post, User
from werkzeug.urls import url_parse
from app import db


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    post_form = PostForm()
    if post_form.validate_on_submit():
        new_post = Post(author=current_user, body=post_form.body.data)
        db.session.add(new_post)
        db.session.commit()
        flash('your post is alive now')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POST_PER_PAGE'], False).items
    return render_template('index.html', title='Home', posts=posts,
                           post_form=post_form)


@app.route('/explorer')
@login_required
def explorer():
    page = request.args.get('page', 1, int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POST_PER_PAGE'], False)

    next_url = url_for(
        'explorer', page=posts.next_num)if posts.has_next else None
    prev_url = url_for(
        'explorer', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Explorer', posts=posts.items,
                           prev_url=prev_url, next_url=next_url)


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


@app.route('/user/<username>/', methods=['GET'])
@login_required
def user_profile(username):
    form = EmptyForm()
    page = request.args.get('page', 1, int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
                            Post.timestamp.desc()).paginate(
                            page, app.config['POST_PER_PAGE'], False)

    next_url = url_for('user_profile', username=username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user_profile', username=username,
                       page=posts.prev_num) if posts.prev_num else None

    return render_template('user_profile.html', title='Profile',
                           posts=posts.items,
                           form=form, user=user, prev_url=prev_url,
                           next_url=next_url)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow_user(username):
    form = EmptyForm()
    if form.validate_on_submit():
        followed_user = User.query.filter_by(username=username).first()
        if followed_user is not None:
            if current_user.id == followed_user.id:
                flash('you cannot follow yourself', category='warning')
            else:
                current_user.follow(followed_user)
                db.session.commit()
                flash(f'you are now following {followed_user.username}')
                return redirect(url_for('user_profile', username=username))
        else:
            return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow_user(username):
    form = EmptyForm()
    if form.validate_on_submit():
        followed_user = User.query.filter_by(username=username).first()
        if followed_user is not None:
            current_user.unfollow(followed_user)
            db.session.commit()
            flash(f'you have unfollowd this user {followed_user.username}')
            return redirect(url_for('user_profile', username=username))
        else:
            return redirect(url_for('index'))
