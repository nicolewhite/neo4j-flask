---
layout: default
title: The Data Model
index: 4
---

# The Data Model

To store information about our users and their acitivites on or our social blogging application, let's think about how we'll want to model this data. For this example, we'll have User, Post, and Tag nodes. Conceptually, we want to capture users publishing posts, tags tagging posts, and users liking posts. In Neo4j, this will look like:

<img width="100%" height="100%" src="http://i.imgur.com/9Nuvbpz.png">

Before beginning, we'll want to create some uniqueness constraints (which will also create indexes). We don't want any duplicate users, posts, or tags, so run the following in the Neo4j Browser or shell:

```
CREATE CONSTRAINT ON (u:User) ASSERT u.username IS UNIQUE;
CREATE CONSTRAINT ON (p:Post) ASSERT p.id IS UNIQUE;
CREATE CONSTRAINT ON (t:Tag) ASSERT t.name IS UNIQUE;
```

Next, we'll go through each view defined in `views.py` and discuss the corresponding logic in `models.py`.

<p align="right"><a href="{{ site.baseurl }}/pages/register-a-user.html">Next: Register a User</a></p>