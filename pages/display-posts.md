---
layout: default
title: Display Posts
index: 8
---

# Display Posts

On both the home page (the `/` view) and a user's profile page (the `/profile/<username>` view), a series of posts is displayed. On the home page, the five most recent posts by all users are displayed; on a user's profile, the five most recent posts by that user are displayed. The following functions in `models.py` retrieve these posts:

```python
# For the / view.
def get_todays_recent_posts():
    query = """
    MATCH (post:Post {date: {today}}),
          (user:User)-[:PUBLISHED]->(post),
          (tag:Tag)-[:TAGGED]->(post)
    RETURN user.username AS username,
           post.id AS id,
           post.date AS date,
           post.timestamp AS timestamp,
           post.title AS title,
           post.text AS text,
           COLLECT(tag.name) AS tags
    ORDER BY timestamp DESC
    LIMIT 5
    """

    posts = graph.cypher.execute(query, today = date())
    return posts

# For the profile/<username> view.
def get_users_recent_posts(username):
    query = """
    MATCH (:User {username:{username}})-[:PUBLISHED]->(post:Post),
          (tag:Tag)-[:TAGGED]->(post)
    RETURN post.id AS id,
           post.date AS date,
           post.timestamp AS timestamp,
           post.title AS title,
           post.text AS text,
           COLLECT(tag.name) AS tags
    ORDER BY timestamp DESC
    LIMIT 5
    """

    posts = graph.cypher.execute(query, username=username)
    return posts
```

The results of [`Graph.cypher.execute()`](http://py2neo.org/2.0/cypher.html#py2neo.cypher.CypherResource.execute) is a [`RecordList`](http://py2neo.org/2.0/cypher.html#py2neo.cypher.RecordList), of which each element is a [`Record`](http://py2neo.org/2.0/cypher.html#py2neo.cypher.Record). The elements of the `Record` can be accessed by attribute or key.

In the templates of `index.html` (shown in the previous section) and `profile.html` (shown in the next section), you'll see that we include the `display_posts.html` template with 

{% raw %}
```
{% include "display_posts.html" %}
```
{% endraw %}

`display_posts.html` looks like this, and using `include` simply inserts this code:

{% raw %}
```html
<ul class=posts>
{% for post in posts %}
  <li>
    <b>{{ post.title }}</b>
      {% if request.path == '/' %}
    by <a href="{{ url_for('profile', username=post.username) }}">{{ post.username }}</a>
      {% endif %}
    on {{ post.date }}
    <a href="{{ url_for('like_post', post_id=post.id) }}">like</a><br>
    <i>{{ ', '.join(post.tags) }}</i><br>
    {{ post.text }}
{% else %}
  <li>There aren't any posts yet!
{% endfor %}
</ul>
``` 
{% endraw %}

Notice that we check that we're on the home page with `if request.path == '/'`. If we're on the home page, we display the username of the user who published the post since the home page will display posts from multiple users. Otherwise, if we're on a user's profile page, we omit this since the profile page only displays posts for one user (the user whose profile you're visiting).

When returning a collection in Cypher, e.g. `COLLECT(DISTINCT tag.name) AS tags`, it is returned as a list in Python. A minimal amount of Python code can be used within the templates; above, I use `', '.join(post.tags)` to convert the list to a string where the values are separated by commas.

Finally, notice that a link titled 'like' is next to each post. This allows users to like a post, which is explained in the next section.

<p align="right"><a href="{{ site.baseurl }}/pages/like-a-post.html">Next: Like a Post</a></p>