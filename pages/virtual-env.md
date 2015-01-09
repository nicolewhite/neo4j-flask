---
layout: default
index: 1
title: Virtual Environments
---

# Virtual Environments

Before beginning, you'll want to set up a Python virtual environment so you don't affect any of your other Python projects. For example, you might use py2neo 1.6.4 for one project and py2neo 2.0.0 for another. Virtual environments ensure your application is using the desired version of the installed packages.

The [documentation](http://docs.python-guide.org/en/latest/dev/virtualenvs/) on virtual environments is a good read if you are unfamiliar with this workflow. To set up a virtual environment for this project, we'll first install `virtualenv` with `pip`:

```
pip install virtualenv
```

Then, we'll create a virtual environment named `neo4j-blog` and activate it:

```
virtualenv neo4j-blog
source neo4j-blog/bin/activate
```

Once activated, you'll notice your shell prompt has changed to reflect which virtual environment you're currently in.

With `pip freeze`, we can see that we've started with a clean slate (when it comes to our Python packages):

```
pip freeze
```


```
wsgiref==0.1.2
```

<p align="right"><a href="{{ site.baseurl }}/pages/required-packages.html">Next: Required Packages</a></p>