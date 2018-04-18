Chapter 6. Building a Quora like site
--------------------------------------------------

Topics in this chapter:
=======================

We have covered basics in last few chapters, like Generic Views, template languages, ORM, interaction with django admin etc. Now in this chapter we will be creating :code:`Custom User`, who will be able to access the Qusetion and answers in the Quora like app.


Quora like Application:
=======================

We have checked Quora for checking many qusetions in our past. Qusetions may be both technical or non technical. In this tutorial we will be creating a Qura like application but not exactly the Quora.

Application Includes:
======================

* Registering custom users (Substitute of django's admin user)
* Custom Users Login/Logout Functionality
* Questions asked by users.
* Answered Questions by Users
* Dashboard user specific.

Django features to learn in this chapter:
==========================================
* Class Based Views
* Basics of Django Testing
* Customising Users

Lets Begin:
===========

We will be creating a project from scratch, lets brush-up !!!

.. sourcecode:: bash

    $ django-admin startproject quora
    $ cd quora
    $ python manage.py startapp core // Custom User Trick

.. note::
    Never user the built-in Django User model directly, even if the built-in Django User implementation fulfill all the requirements of your application. *Once you are done with customising your Custom user then only do makemigrations & migrate*

Make custom user:
=================
* Step 1): Goto :code:`core/models.py` and add this
.. sourcecode:: python

    from django.db import models
    from django.contrib.auth.models import AbstractUser


    class User(AbstractUser):
        pass

* Step 2): In your settings.py file add a line just after ALLOWED_HOSTS = [].

.. sourcecode:: python

    AUTH_USER_MODEL = 'core.User' // It can be kept anywhere in the file but good to keep just after Allowed hosts.

.. note::
    Don't forget to add your newly created app to installed apps in :code:`settings.py` file.

.. sourcecode:: python

    INSTALLED_APPS = [
        'django.contrib.admin',
        . . .
        . . .
        'core',
    ]

Congratulations you have customised your Django user Model. now lets migrate changes.

.. sourcecode:: bash

    $ python manage.py makemigrations
    $ python manage.py migrate
