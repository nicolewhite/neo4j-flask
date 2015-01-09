---
layout: default
title: Similarities Between Users
index: 10
---

When a user visits their own profile, we want to recommend other users whose posts the logged-in user might enjoy reading. To do so, we'll write a Cypher query that finds users most similar to the logged-in user based on the number of tags they've mutually posted about. On the other hand, when the logged-in user visits another user's profile, we want to display what the two users have in common. For this, we'll write a Cypher query that finds how many of the logged-in user's posts the other user has liked, along with which tags they've mutually posted about. The `/profile/<username>` view is defined in `views.py`:

```python
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
        # If they're visiting another user's profile, 
        # show what they have in common with that user.
        else:
            common = user.get_commonality_of_user(username)

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
        MATCH (u1:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
              (u2:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        WHERE u1.username = {username} AND u1 <> u2
        WITH u1, u2, COLLECT(DISTINCT tag.name) AS tags
        WITH u2, tags, LENGTH(tags) AS len
        ORDER BY len DESC
        LIMIT 3
        RETURN u2.username AS similar_user, tags
        """

        similar = graph.cypher.execute(query, username=self.username)
        return similar

    def get_commonality_of_user(self, username):
        # Find how many of the logged-in user's posts the other user
        # has liked and which tags they've both blogged about.
        query = """
        MATCH (user1:User {username:{user_viewing}}),
              (user2:User {username:{user_loggedin}})
        OPTIONAL MATCH (user1)-[:LIKED]->(post:Post)<-[:PUBLISHED]-(user2)
        OPTIONAL MATCH (user1)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
                       (user2)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        RETURN COUNT(DISTINCT post) AS likes, 
        	     COLLECT(DISTINCT tag.name) AS tags
        """

        result = graph.cypher.execute(query,
                                      user_viewing=username,
                                      user_loggedin=self.username)

        result = result[0]
        common = dict()
        common['likes'] = result.likes
        common['tags'] = result.tags if len(result.tags) > 0 else None
        return common
```

Both `common` and `similar` are passed to the `profile.html` template, which displays whichever is appropriate (`similar` is diplayed if the user is viewing their own profile, and `common` is displayed if they're visiting someone else's profile):

{% raw %}
```html
{% extends "layout.html" %}
{% block body %}

<h2>{{ username }}'s profile</h2>

{% if session.logged_in %}
    {% if session.username == username %}
        <h3>Users similar to you:</h3>

          {% for user in similar %}
            <p>
            <a href="{{ url_for('profile', username=user.similar_user) }}">{{ user.similar_user }}</a>
            also blogs about <i>{{ ', '.join(user.tags) }}</i>
            </p>
          {% else %}
            <p>There aren't any users who've blogged about the same tags as you!</p>
          {% endfor %}

        <h3>Your recent posts:</h3>

    {% else %}

  <p>{{ username }} has liked {{ common.likes }} of your posts and
      {% if common.tags %}
      also blogs about <i>{{ ', '.join(common.tags) }}</i>
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

If a user is visiting their own profile, similar users are displayed with links to their profiles.

<p align="right"><a href="{{ site.baseurl }}/pages/logout-a-user.html">Next: Logout a User</a></p>