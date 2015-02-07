---
layout: default
title: Project Structure
index: 3
---

# Project Structure

The Explore Flask book provides [great documentation](https://exploreflask.com/organizing.html) on best-practices for organizing your project. For this sample blogging application, we're going to keep it relatively simple:

```
run.py
requirements.txt
blog/
	__init__.py
	models.py
	views.py
	static/
		style.css
	templates/
		index.html
		register.html
		login.html
		logout.html
		profile.html
		display_posts.html
```

Recall that we created `requirements.txt` in the previous step. Typically, the bulk of the action will take place in `models.py` (where we'll define classes, methods, etc.) and `views.py` (where we'll define our 'views', or site pages). The `__init__.py` file in the `blog/` directory allows it to be used as a [package](https://exploreflask.com/organizing.html#package).

According to the linked documentation, `__init__.py` within the `blog` directory should be used to "initialize your application and bring together all of the various components." My `__init__.py` thus looks like this:

```python
from flask import Flask

app = Flask(__name__)

import models
import views
```

`run.py` is "the file that is invoked to start up a development server. It gets a copy of the app from your package and runs it. This won’t be used in production, but it will see a lot of mileage in development." My `run.py` file looks like this:

```python
from blog import app
import os

app.secret_key = os.urandom(24)
app.run(debug=True)
```

Setting the app's `secret_key` allows you to use sessions, which will be explained later. Setting `debug` to `True` allows you to see the stacktrace when anything goes wrong. When putting your application into production, however, `debug` should be set to `False`. At the end of the tutorial, we'll start our sample blog with `python run.py` and navigate to [http://localhost:5000](http://localhost:5000).

The `blog/static` directory contains all CSS, JavaScript, and images, and the `blog/templates` directory contains all your Jinja2 templates.

<p align="right"><a href="{{ site.baseurl }}/pages/the-data-model.html">Next: The Data Model</a></p>