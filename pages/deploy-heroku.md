---
layout: default
title: Deploy to Heroku
index: 14
---

# Deploy to Heroku

To deploy your application to Heroku, you should first read their [getting started with Python guide](https://devcenter.heroku.com/articles/getting-started-with-python#introduction) so that you are familiar with the deployment process.

Within the same directory that your application sits, 

We need to make a few modifications and additions. First, change `run.py` to the following:

```python
from blog import *
import os

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
```

This will get the `$PORT` environment variable for port assignment. Next, change the initilization of `graph` in `models.py` to the following:

```python
graph = Graph(os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474') + '/db/data/')
```

This will get the `$GRAPHENEDB_URL` environment variable