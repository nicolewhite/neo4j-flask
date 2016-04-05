---
layout: default
title: The Data Model
index: 4
---

# The Data Model

To store information about our users and their activities on or our social blogging application, let's think about how we'll want to model this data. For this example, we'll have `:User`, `:Post`, and `:Tag` labels for our nodes. Conceptually, we want to capture:

* users publishing posts, or `(:User)-[:PUBLISHED]->(:Post)`
* tags tagging posts, or `(:Tag)-[:TAGGED]->(:Post)`
* users liking posts, or `(:User)-[:LIKED]->(:Post)`

<img width="100%" height="100%" src="http://i.imgur.com/9Nuvbpz.png">

Before beginning, we'll want to create uniqueness constraints for the appopriate label and property pairs. This will also create indexes on these label and property pairs. We don't want any duplicate `:User`, `:Post`, or `:Tag` nodes, so `blog/__init__.py` contains the following and is run when the app is started:

```python
from .views import app
from .models import graph

def create_uniqueness_constraint(label, property):
    query = "CREATE CONSTRAINT ON (n:{label}) ASSERT n.{property} IS UNIQUE"
    query = query.format(label=label, property=property)
    graph.cypher.execute(query)

create_uniqueness_constraint("User", "username")
create_uniqueness_constraint("Tag", "name")
create_uniqueness_constraint("Post", "id")
```

With a uniqueness constraint on the `:User` label by the `username` property, Neo4j ensures there are never `:User` labeled nodes that share the same `username`. Any transactions that violate this constraint will be rejected. The same applies to the uniquess constraints on `:Tag` by `name` and `:Post` by `id`.

Next, we'll go through each view defined in `views.py` and discuss the corresponding logic in `models.py`.

<p align="right"><a href="{{ site.baseurl }}/pages/register-a-user.html">Next: Register a User</a></p>