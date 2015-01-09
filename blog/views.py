from . import app
from models import *
from flask import request, session, redirect, url_for, \
    abort, render_template, flash

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
        elif not User(username).set_password(password).register():
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

        if not user.find():
            error = 'A user with that username does not exist.'
        elif not user.verify_password(password):
            error = 'That password is incorrect.'
        else:
            session['username'] = user.username
            flash('Logged in.')
            return redirect(url_for('index', username=username))

    return render_template('login.html', error=error)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('index'))

@app.route('/add_post/<username>', methods=['POST'])
def add_post(username):
    user = User(session['username'])
    title = request.form['title']
    text = request.form['text']
    tags = request.form['tags']

    if title == '':
        abort(400, 'You must give your post a title.')
    if tags == '':
        abort(400, 'You must give your post at least one tag.')
    if text == '':
        abort(400, 'You must give your post a texy body.')

    user.add_post(title, tags, text)
    return redirect(url_for('index'))

@app.route('/like_post/<post_id>', methods=['GET'])
def like_post(post_id):
    user = User(session['username'])
    user.like_post(post_id)
    flash('Liked post.')
    return redirect(request.referrer)

@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    posts = get_users_recent_posts(username)

    similar = []
    common = []

    if session.get('username'):
        user = User(session['username'])
        # If they're visiting their own profile, show similar users.
        if user.username == username:
            similar = user.get_similar_users()
        # If they're visiting another user's profile, show what they have in common
        # with that user.
        else:
            common = user.get_commonality_of_user(username)

    return render_template(
        'profile.html',
        username=username,
        posts=posts,
        similar=similar,
        common=common
    )