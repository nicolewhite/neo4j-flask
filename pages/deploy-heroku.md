---
layout: default
title: Deploy to Heroku
index: 14
---

# Deploy to Heroku

To deploy your application to Heroku, you should first read their [getting started with Python guide](https://devcenter.heroku.com/articles/getting-started-with-python#introduction) so that you are familiar with the deployment process.

Within the same directory that your application sits, in the terminal, execute `heroku create`. This will create a new git remote called `heroku`. Next, you need to add the [GrapheneDB add-on](https://devcenter.heroku.com/articles/graphenedb), which is an easy way to get set up with a Neo4j database on Heroku.

```
heroku addons:add graphenedb:chalk
```

Next, you need to add a file in the root directory called `Procfile`, a text file with the following:

```
web: python run.py
```

This'll tell Heroku to run `run.py` to start your application. We need to make a few modifications and additions to `run.py`:

```python
from blog import *
import os

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
```

This will get the `$PORT` environment variable from your Heroku configuration for port assignment. Note that `debug=True` is gone. You don't want to expose your stacktrace in production. Next, change the initilization of `graph` in `models.py` to the following:

```python
graph = Graph(os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474') + '/db/data/')
```

This will get the `$GRAPHENEDB_URL` environment variable that is present in your Heroku configuation after adding the GrapheneDB add-on.

Finally, `git push heroku master` will deploy your application.