---
layout: default
title: Add a Post
index: 7
---

# Add a Post

Once a user has successfully logged in, they're redirected to the `/` view, the home page. When `session.username` is not `None`, a form is displayed that allows the user to share a post. This form sends a `POST` request with the title, text, and tags of the post to the `/add_post/<username>` view, where `<username>` is replaced with the logged-in-user's username. In `views.py`, this view is defined by the following:

```python
@app.route('/add_post', methods=['POST'])
def add_post():
    user = User(session['username'])
    title = request.form['title']
    tags = request.form['tags']
    text = request.form['text']

    if title == '':
        abort(400, 'You must give your post a title.')
    if tags == '':
        abort(400, 'You must give your post at least one tag.')
    if text == '':
        abort(400, 'You must give your post a texy body.')

    user.add_post(title, tags, text)
    return redirect(url_for('index'))
```

First, a `User` object is initialized with the logged-in-user's username. Then, the title, text, and tags that were sent with the `POST` request are accessed and checked to make sure they aren't empty. If it all checks out, the `User.add_post()` method is called with `title`, `text`, and `tags` as arguments. The `add_post()` method is defined in the `User` class like so:

```python
class User:

	...

    def add_post(self, title, tags, text):
        import uuid

        user = self.find()
        post = Node(
            "Post",
            id=str(uuid.uuid4()),
            title=title,
            text=text,
            timestamp=timestamp(),
            date=date()
        )
        rel = Relationship(user, "PUBLISHED", post)
        graph.create(rel)

        tags = [x.strip() for x in tags.lower().split(',')]
        for t in tags:
            tag = graph.merge_one("Tag", "name", t)
            rel = Relationship(tag, "TAGGED", post)
            graph.create(rel)
```

The user is found in the database with `User.find()`, which returns a `py2neo.Node` object. Then, another `Node` object `post` is created with the shown properties. A random id is generated with the `uuid` package's [`uuid4()`](https://docs.python.org/2/library/uuid.html#uuid.uuid4) method, and the timestamp and date are set with functions I defined elsewhere in `models.py`:

```python
from datetime import datetime

def timestamp():
    unix = int(datetime.now().strftime('%s'))
    return unix

def date():
    today = datetime.now().strftime('%Y-%m-%d')
    return today
```

With both the `user` and `post` variables, we can create a `(:User)-[:PUBLISHED]->(:Post)` relationship in the graph by passing a [`py2neo.Relationship`](http://py2neo.org/2.0/essentials.html#relationships) object to `Graph.create()`. Finally, the tags are split on commas and lowercased. For each of these tags, a relationship `(:Tag)-[:TAGGED]->(:Post)` is created. We use the `Graph.merge_one()` method to ensure we are finding or creating a `Tag` node with the given `name` property.

The form where a user adds a new post is located in `index.html`:

{% raw %}
```html
{% extends "layout.html" %}
{% block body %}

<h2>Home</h2>
  {% if session.username %}
    <h3>Share New Post</h3>
    <form action="{{ url_for('add_post') }}" method=post>
        <dl>
            <dt>Title:</dt>
            <dd><input type=text size=30 name=title></dd>
            <dt>Tags (separated by commas):</dt>
            <dd><input type=text size=30 name=tags></dd>
            <dt>Text:</dt>
            <dd><textarea name=text rows=5 cols=40></textarea></dd>
        </dl>
        <input type=submit value=Share>
    </form>
  {% endif %}

<br>

<h3>Today's Recent Posts</h3>
{% include "display_posts.html" %}

{% endblock %}
```
{% endraw %}

<p align="right"><a href="{{ site.baseurl }}/pages/display-posts.html">Next: Display Posts</a></p>