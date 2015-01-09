---
layout: default
title: Logout a User
index: 11
---

# Logout a User

When all the fun is over, a user logs out by clicking the logout link at the top of the page, which sends a `GET` request to the `/logout` view:

```python
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('index'))
```

This removes `username` from the session and takes the visitor back to the home page. Once logged out, the visitor won't see any of the similarities shown in the previous section when visiting their own or someone else's profile.