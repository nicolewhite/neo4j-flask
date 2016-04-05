---
layout: default
title: Similarities Between Users
index: 10
---

# Similarities Between Users

When a user visits their own profile, we want to recommend other users whose posts the logged-in user might enjoy reading. To do so, we'll write a Cypher query that finds users most similar to the logged-in user based on the number of tags they've mutually posted about. On the other hand, when the logged-in user visits another user's profile, we want to display what the two users have in common. For this, we'll write a Cypher query that finds how many of the logged-in user's posts the other user has liked, along with which tags they've mutually posted about. The `/profile/<username>` view is defined in `views.py`:

```python
@app.route('/profile/<username>')
def profile(username):
    logged_in_username = session.get('username')
    user_being_viewed_username = username

    user_being_viewed = User(user_being_viewed_username)
    posts = user_being_viewed.get_recent_posts()

    similar = []
    common = []

    if logged_in_username:
        logged_in_user = User(logged_in_username)

        if logged_in_user.username == user_being_viewed.username:
            similar = logged_in_user.get_similar_users()
        else:
            common = logged_in_user.get_commonality_of_user(user_being_viewed)

    return render_template(
        'profile.html',
        username=username,
        posts=posts,
        similar=similar,
        common=common
    )
```

In `models.py`:

```python
class User:

	...
  
    def get_similar_users(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = """
        MATCH (you:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
              (they:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        WHERE you.username = {username} AND you <> they
        WITH they, COLLECT(DISTINCT tag.name) AS tags, COUNT(DISTINCT tag) AS len
        ORDER BY len DESC LIMIT 3
        RETURN they.username AS similar_user, tags
        """

        return graph.cypher.execute(query, username=self.username)

    def get_commonality_of_user(self, other):
        # Find how many of the logged-in user's posts the other user
        # has liked and which tags they've both blogged about.
        query = """
        MATCH (they:User {username: {they} })
        MATCH (you:User {username: {you} })
        OPTIONAL MATCH (they)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
                       (you)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        RETURN SIZE((they)-[:LIKED]->(:Post)<-[:PUBLISHED]-(you)) AS likes,
               COLLECT(DISTINCT tag.name) AS tags
        """

        return graph.cypher.execute(query, they=other.username, you=self.username)[0]
```

Both `common` and `similar` are passed to the `profile.html` template, which displays whichever is appropriate. `similar` is diplayed if the user is viewing their own profile, and `common` is displayed if they're visiting someone else's profile:

{% raw %}
```html
{% extends "layout.html" %}
{% block body %}

<h2>{{ username }}'s profile</h2>

{% if session.username %}
    {% if session.username == username %}
        <h3>Users similar to you:</h3>

          {% for user in similar %}
            <p>
            <a href="{{ url_for('profile', username=user.similar_user) }}">{{ user.similar_user }}</a>
            also blogs about <i>{{ ", ".join(user.tags) }}</i>
            </p>
          {% else %}
            <p>There aren't any users who've blogged about the same tags as you!</p>
          {% endfor %}

        <h3>Your recent posts:</h3>

    {% else %}

  <p>{{ username }} has liked {{ common.likes }} of your posts and
      {% if common.tags %}
      also blogs about <i>{{ ", ".join(common.tags) }}</i>
      {% else %}
      hasn't blogged about any of the same tags
      {% endif %}
  </p>

  <h3>{{ username }}'s recent posts:</h3>

    {% endif %}
{% endif %}

{% include "display_posts.html" %}

{% endblock %}
```
{% endraw %}

<p align="right"><a href="{{ site.baseurl }}/pages/logout-a-user.html">Next: Logout a User</a></p>