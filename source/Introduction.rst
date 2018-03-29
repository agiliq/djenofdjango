Chapter 1: Introduction
------------------------

Virtual Environment (The Saviour)
==================================

The best time to learn about virtual environment is when you are a beginner in learning python/django as it will be very much helpful.

* **What is virtual environment ?**

    A virtual environment is a way for you to have multiple versions of python on your machine without them clashing with each other, each version can be considered as a development environment and you can have different versions of python libraries and modules all isolated from one another. For more information visit `virtualenv <https://virtualenv.pypa.io/en/stable/>`_

* **Importance of virtual environment.**

    Say, if you're working on an open source project that uses :code:`django 1.7` but locally, you installed :code:`django 2.0` for other project. It's almost impossible for you to contribute to open source because you'll get a lot of errors due to the difference in django versions. If you decide to downgrade to :code:`django 1.7` then you can't work on your project anymore because that depend on :code:`django 2.0`. Virtual environment lets you handle this situation by creating a separate virtual(development) environments that are not tied together and can be activated/deactivated easily whenever you want.

* **How does virtual environment work ?** ::

    $ virtualenv venv
    $ cd venv
    $ source bin/activate
    (venv)$                 // The current shell starts using the virtual environment.
    (venv)$ deactivate      // virtual environment deactivated.

Downloading and Installing
==========================

    Backwards compatibility, python version compatiblity, common issues etc.

What is Django?
===============

    Brief History
    What django aims to be, what it is not (not a cms or ready to use website)
    Batteries included
    Future

Django Features:
================

    Structure
    Reusable Code
    Security
    Documentation
    Community

Why Django? Why Django instead of any other framework?
======================================================

    Compare django to other lightweight frameworks like flask and rails.

Inside Django
=============

    Python Philosophy
    Django Philosophy
    Request-Response cycle
    Django Architecture
    Django ORM
    DRY principle
    Loose coupling
    Introduction to middleware, template tags, context processors, RequestContext

