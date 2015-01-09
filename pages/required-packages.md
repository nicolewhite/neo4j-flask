---
layout: default
title: Required Packages
index: 2
---

# Required Packages

For our sample blogging application, we'll need to install Flask, py2neo, passlib, and bcrypt:

```
pip install flask
pip install py2neo
pip install passlib
pip install bcrypt
```

If we execute `pip freeze` again, we'll see that we have a lot more packages installed now:

```
pip freeze
```

```
Flask==0.10.1
Jinja2==2.7.3
MarkupSafe==0.23
Werkzeug==0.9.6
bcrypt==1.1.0
cffi==0.8.6
itsdangerous==0.24
passlib==1.6.2
py2neo==2.0.3
pycparser==2.10
six==1.9.0
wsgiref==0.1.2
```

As suggested by Flask's documentation, these dependencies should be stored in a text file called `requirements.txt`:

```
pip freeze > requirements.txt
```

<p align="right"><a href="{{ site.baseurl }}/pages/project-structure.html">Next: Project Structure</a></p>