---
layout: default
title: Register a User
index: 5
---

# Register a User

Before any content can be created on our blog, users will need to be able to sign up for an account. When successful, this will create a `User` node in the database with the properties `username` and `password`, where the password is hashed.

The registration page is located at `/register` and will accept both `GET` and `POST` requests. A `GET` request will be sent when a visitor lands on the page, and a `POST` request will be sent when they fill out the registration form. In `views.py`, the `/register` view is defined by the following:

```python
from . import app
from models import *
from flask import request, session, redirect, url_for, \
    abort, render_template, flash

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
```

The `request` variable is a Flask object that parses the incoming request, allowing you to access the request's data. For example, the method of the request (either `GET` or `POST` or whatever is allowed) is stored on `request.method`. As I said before, when a user lands on the page a `GET` request is sent. When a user fills out the registration form, a `POST` request is sent. This view checks the method type, and if it is a `GET` request it simply returns the template `register.html`. However, if it is a `POST` request, the `username` and `password` are parsed from the request and a user is created if their inputs meet all of the criteria. To understand this better, we'll have to look at part of the `User` class that was defined in `models.py`:

```python
from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt

graph = Graph()

class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = graph.find_one("User", "username", self.username)
        return user

    def set_password(self, password):
        self.password = bcrypt.encrypt(password)
        return self

    def register(self):
        if not self.password:
            return False
        elif not self.find():
            user = Node("User", username=self.username, password=self.password)
            graph.create(user)
            return True
        else:
            return False
```

An object of class `User` is initialized with a `username` argument. The `User.find()` method uses py2neo's [`Graph.find_one()`](http://py2neo.org/2.0/essentials.html#py2neo.Graph.find_one) method to find a node in the database with label User and the given username, returning a `py2neo.Node` object. Recall that a uniqueness constraint was created for User nodes based on the username property, so there will not be more than one user with the given username. The `User.set_password()` method encrypts the given password and stores it on the `User` object. Finally, the `User.register()` method first checks if a password has been set. Then, if a password has been set, it checks if a user with that username already exists in the database. If not, then a user is created with the given username and password by passing the [`py2neo.Node`](http://py2neo.org/2.0/essentials.html#nodes) object to the [`Graph.create()`](http://py2neo.org/2.0/essentials.html#py2neo.Graph.create) method. `True` is returned to indicate that the registration was successful.

Finally, to fully understand the registration procedure we should take a look at the `register.html` template:

{% raw %}
```html
{% extends "layout.html" %}
{% block body %}
  <h2>Register</h2>
  {% if error %}
  <p class=error><strong>Error:</strong> {{ error }}
  {% endif %}
	<form action="{{ url_for('register') }}" method=post>
		Username:<br>
		<input type="text" name="username">
		<br>
		Password:<br>
		<input type="password" name="password">
		<input type="submit" value="Register">
	</form>
{% endblock %}
```
{% endraw %}

Recall in `views.py` that the `register()` method defined a variable `error` with a string telling the user what they did wrong. The variables passed along with `render_template()` can be accessed with the double curly braces in the respective template `.html` file. If `error` is not `None`, then it is displayed to the visitor. The form sends a `POST` request to the `/register` view due to {% raw %}`action="{{ url_for('register') }}"`{% endraw %}, where [`url_for()`](http://flask.pocoo.org/docs/0.10/api/#flask.url_for) is a Flask method for accessing URLs defined in view functions. The form's data is accessed with the input's names; for example, the string that the user types into the `username` text box is accessed with `request.form['username']` in `views.py`.

<p align="right"><a href="{{ site.baseurl }}/pages/login-a-user.html">Next: Login a User</a></p>