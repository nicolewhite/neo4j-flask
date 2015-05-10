from models import User, get_users_recent_posts, get_todays_recent_posts
from flask import Flask, request, session, redirect, url_for, \
    abort, render_template, flash

app = Flask(__name__)

@app.route('/')
def index():
    posts = get_todays_recent_posts()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(username) < 1:
            error = 'Your username must be at least one character.'
        elif len(password) < 5:
            error = 'Your password must be at least 5 characters.'
        elif not User(username).register(password):
            error = 'A user with that username already exists.'
        else:
            flash('Successfully registered. Please login.')
            return redirect(url_for('login'))

    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username)

        if not user.verify_password(password):
            error = 'Invalid login.'
        else:
            session['username'] = user.username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('index'))

@app.route('/add_post', methods=['POST'])
def add_post():
    user = User(session['username'])
    title = request.form['title']
    tags = request.form['tags']
    text = request.form['text']

    if not title:
        abort(400, 'You must give your post a title.')
    if not tags:
        abort(400, 'You must give your post at least one tag.')
    if not text:
        abort(400, 'You must give your post a texy body.')

    user.add_post(title, tags, text)
    return redirect(url_for('index'))

@app.route('/like_post/<post_id>')
def like_post(post_id):
    username = session.get('username')
    if not username:
        abort(400, 'You must be logged in to like a post.')

    user = User(username)
    user.like_post(post_id)
    flash('Liked post.')
    return redirect(request.referrer)

@app.route('/profile/<username>')
def profile(username):
    posts = get_users_recent_posts(username)

    similar = []
    common = []

    viewer_username = session.get('username')

    if viewer_username:
        viewer = User(viewer_username)
        if viewer.username == username:
            similar = viewer.get_similar_users()
        else:
            common = viewer.get_commonality_of_user(username)

    return render_template(
        'profile.html',
        username=username,
        posts=posts,
        similar=similar,
        common=common
    )