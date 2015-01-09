---
layout: default
title: Logout a User
index: 10
---

# Logout a User

When all the fun is over, a user logs out by clicking the logout link at the top of the page, which sends a `GET` request to the `/logout` view:

```python
@app.route('/logout', methods=['GET'])
def logout():
	session.pop('logged_in', None)
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('index'))
```