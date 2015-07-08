---
layout: default
title: Display Posts
index: 8
---

# Display Posts

On both the home page (the `/` view) and a user's profile page (the `/profile/<username>` view), a series of posts is displayed. On the home page, the five most recent posts by all users are displayed; on a user's profile, the five most recent posts by that user are displayed. The function `get_todays_recent_posts` gets today's most recent posts and the method `User.get_recent_posts` gets a user's most recent posts.

```python
def get_todays_recent_posts():
    query = """
    MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
    WHERE post.date = {today}
    RETURN user.username AS username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT 5
    """

    return graph.cypher.execute(query, today=date())
```

```python
class User:

  ...

  def get_recent_posts(self):
    query = """
    MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
    WHERE user.username = {username}
    RETURN post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT 5
    """

    return graph.cypher.execute(query, username=self.username)
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
<ul class="posts">
{% for row in posts %}
  <li>
    <b>{{ row.post.title }}</b>
      {% if request.path == "/" %}
    by <a href="{{ url_for('profile', username=row.username) }}">{{ row.username }}</a>
      {% endif %}
    on {{ row.post.date }}
    <a href="{{ url_for('like_post', post_id=row.post.id) }}">like</a><br>
    <i>{{ ", ".join(row.tags) }}</i><br>
    {{ row.post.text }}
{% else %}
  <li>There aren't any posts yet!
{% endfor %}
</ul>
```
{% endraw %}

Notice that we check that we're on the home page with `if request.path == "/"`. If we're on the home page, we display the username of the user who published the post since the home page will display posts from multiple users. Otherwise, if we're on a user's profile page, we omit this since the profile page only displays posts for one user (the user whose profile you're visiting).

When returning a collection in Cypher, e.g. `COLLECT(DISTINCT tag.name) AS tags`, it is returned as a list in Python. A minimal amount of Python code can be used within the templates; above, I use `", ".join(row.tags)` to convert the list to a string where the values are separated by commas.

Finally, notice that a link titled 'like' is next to each post. This allows users to like a post, which is explained in the next section.

<p align="right"><a href="{{ site.baseurl }}/pages/like-a-post.html">Next: Like a Post</a></p>
