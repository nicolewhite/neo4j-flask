---
layout: default
title: Login A User
index: 6
---

# Login A User

Now that users are able to register for an account, we can define the view that allows them to login to the site and start a [session](http://flask.pocoo.org/docs/0.10/quickstart/#sessions). In `views.py`, my `/login` view is defined by the following:

```python
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
            session['logged_in'] = True
            session['username'] = user.username
            flash('Logged in.')
            return redirect(url_for('profile', username=username))

    return render_template('login.html', error=error)
```

The code here should look similar to the `/register` view. There is a similar form to fill out on `login.html`, where a user types in their username and password. With the given username, a `User` object is initialized. If the user is not found, then we tell the user that a user with that username does not exist. If the user is found, then the password they filled out in the form is [verified against the hashed password](https://pythonhosted.org/passlib/lib/passlib.hash.bcrypt.html) stored on the `User` node in the database. If the verification is successful, a `session` object is created and the `username` is set to the given username and `logged_in` is set to `True`. The user is then directed to their profile, which will be shown next. In `models.py`, the `User.verify_password()` method is defined as:

```python
class User:

    ...

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False
```

Note that node properties can be retrieved just as you would retrieve values from a Python dictionary. In this case, I got the password property off of the Node object with `user['password']`.

The `login.html` template is nearly identical to the `register.html` template, with the exception of the form's action (which sends a `POST` request to the `/login` view):

{% raw %}
```html
{% extends "layout.html" %}
{% block body %}
  <h2>Login</h2>
  {% if error %}
  <p class=error><strong>Error:</strong> {{ error }}
  {% endif %}
	<form action="{{ url_for('login') }}" method=post>
		Username:<br>
		<input type="text" name="username">
		<br>
		Password:<br>
		<input type="password" name="password">
		<input type="submit" value="Login">
	</form>
{% endblock %}
```
{% endraw %}