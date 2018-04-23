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
    Never use the built-in Django User model directly, even if the built-in Django User implementation fulfill all the requirements of your application. *Once you are done with customising your Custom user then only do makemigrations & migrate*

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
    $ python manage.py createsuperuser // follow the instructions

We will now create the Custom user's entry in Django Admin, as by the above process we won't be able to see its entry in Django admin's dashboard. So , in :code:`core/admin.py` we should add :

.. sourcecode:: python

    from django.contrib import admin
    from django.contrib.auth.admin import UserAdmin
    from .models import User

    admin.site.register(User, UserAdmin)

Class Based Views
===================

Class-based views provide an alternative way to implement views as Python objects instead of functions. They do not replace function-based views, but have certain differences and advantages when compared to function-based views:

* Organization of code related to specific HTTP methods (GET, POST, etc.) can be addressed by separate methods instead of conditional branching.

* Object oriented techniques such as mixins (multiple inheritance) can be used to factor code into reusable components.

Example

.. sourcecode:: python

    from django.http import HttpResponse
    // Function Based View.
    def my_view(request):
        if request.method == 'GET':
            # <view logic>
            return HttpResponse('result')

    from django.http import HttpResponse
    from django.views import View
    // Class Based View
    class MyView(View):
        def get(self, request):
            # <view logic>
            return HttpResponse('result')

Register Custom User
=====================

Now that we are aware of Class Based View let's implement **user registration using the same**.

Add the below code to :code:`core/forms.py`

.. sourcecode:: python

    from django import forms
    from .models import User

    class RegisterForm(forms.ModelForm):
        password = forms.CharField(widget=forms.PasswordInput())

        class Meta:
            model = User
            fields = ['email', 'first_name', 'last_name', 'password', 'username']

We will now use the above forms in our views, add the below code to :code:`core/views.py`.

.. sourcecode:: python

    from django.shortcuts import render
    from .forms import RegisterForm
    from django.contrib.auth import login
    from django.contrib.auth.hashers import make_password


    class RegisterView(FormView):

        def get(self, request):
            content = {}
            content['form'] = RegisterForm
            return render(request, 'register.html', content)

        def post(self, request):
            content = {}
            form = RegisterForm(request.POST, request.FILES or None)
            if form.is_valid():
                user = form.save(commit=False)
                user.password = make_password(form.cleaned_data['password'])
                user.save()
                login(request, user)
                return redirect(reverse('dashboard-view'))
            content['form'] = form
            template = 'register.html'
            return render(request, template, content)

There are few thing which we have imported like login(), make_password() etc, it will be good to know about them.

* To log a user in, from a view, use :code:`login()`. It takes an HttpRequest object and a User object. login() saves the user’s ID in the session, using Django’s session framework.
* :code:`make_password` creates a hashed password in the format used by this application. It takes one mandatory argument: the password in plain-text.
* we will talk about :code:`dashboard-view` further in this tutorial. For now just relate it like, once you register yourself you will be redirected to the :code:`dashbord-view`.

Its still not over we still have to make some modifications in settings.py , urls.py and adding of templates. If you have followed previous chapters you may try on your own. Still you can refer to content below.

Add below code to :code:`core/urls.py` and :code:`quora/urls.py` respectively.

.. sourcecode:: python

    from django.urls import path
    from .views import RegisterView

    urlpatterns = [
        path('register/', RegisterView.as_view(), name='register-view'),
    ]

    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('core/', include('core.urls')),
    ]

Now we will add a new directory to our project as :code:`project/templates` in our case  :code:`quora/templates`. And inside templates directory add a new file :code:`templates/r`
