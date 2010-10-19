Chapter 5. Building a Wiki
-----------------------------
..
    (Topics introduced: Managing user registration using django-regsitration. Advanced ORM tricks. Overriding save for Entities. Signals. Websearches using Yahoo Devloper API.)

    Diving in. [Code listing]

    Managing user registration using django-regsitration.
    In the previous chapters we did not allow external users to create a user. Here a user can create an account on the wiki. This is managed using django-registration.
    Explanation of Django registration, its views and templates.
    Discussion of making reusable Django applications, taking Django-registration as example.
    
    Advanced ORM
    model.extra, How to use it to handle complex queries.
    Defining customer manager for models. (With a wiki, we reattach model.objects to a manager which only gets the latest object. Another custom manager, model.allobjects gets us all the elements.)
    Manager methods vs. classmethods.
    Overiding save, delete amd other model objects to enable versioning for objects.
    Introduce signals. (However we would not have used this in our code.)
    Show how signals could have been used for the same purpose, and compare.
    
    Websearches using Yahoo Developer API.  
    We want to make the wiki searchable, so instead of going via a local search system like Lucene, we use Yahoo Developer API. In this we can explain to use django.util.simplejson, to talk to external APIs which provide a JSON interface. 
  

A wiki application:
====================

In this chapter, we will build a wiki from scratch. Basic functionality includes:

* User registration

* Article Management (CRUD) with ReST support

* Audit trail for articles

* Revision history

Reusable Apps®:
===============

To manage user registrations, we will use ``django-registration``. You can download it from 

.. note:: http://bitbucket.org/ubernostrum/django-registration/

django-registration is a great example of a reusable app, which can be customized to fit our requirements
while providing the most common pattern by default (sign up, email activation etc)

Some functionality offered by the app:

* User sign-up view

* Activation email view

* Validate activation key and create user account

* Login, logout from ``contrib.auth``

* Management scripts to clear expired registrations

We shall follow the default pattern, i.e. user registration with activation email in the wiki app, although django-registration
allows customization of the process by using ``backends`` which should know how to handle the registration. It ships with two such
backends: ``default`` and ``simple``

.. note:: 

    browse through the code of django-registration to see what urls are avaialbe, what context is passed to the templates,
    which urls are mapped to which views etc.

    Looking at named urls from ``urls.py`` would be useful for creating links to registration, login etc by using 
    the url templatetag.

To install, download the app and run::

    python setup.py install

This will be installed to the site wide python packages directory but can still be imported from our app since it is a
python package.

Now, include ``registration`` in your ``INSTALLED_APPS``, do ``syncdb`` and include the urls:

.. literalinclude:: djen_project/urls.py
    :commit: 2bb5e33

.. note:: django-registration provides views for login at ``accounts/login`` so we can omit
          our previous entry for the same.

The app requires a setting called ``ACCOUNT_ACTIVATION_DAYS`` which is the number of days before which the user should complete
registration. If you are not using ``local_settings.py``, create one and add ``from local_settings import *`` to ``settings.py``. Now
add this setting to local_settings.py::

    # Django registration settings
    ACCOUNT_ACTIVATION_DAYS = 7

Now, ``accounts/register/`` provides the user sign-up view and renders to ``registration/registration_form.html``, so lets write the template:

.. literalinclude:: djen_project/wiki/templates/registration/registration_form.html
    :commit: 3a0af03
    :language: django

Note that ``form`` is the user sign-up form passed as context by ``register`` of django-registration.

To demostrate template heirarchy, we have used a base template and built all other registration templates on top of it. The base template looks like:
``wiki/templates/registration/base.html``

.. literalinclude:: djen_project/wiki/templates/registration/base.html
    :commit: e887a3e
    :language: django

At the moment, we have ``extra_head`` and ``content`` blocks. You can place as many blocks as you like with careful planning and hierarchy. For example
``extra_head`` would serve to include child template specific css/scripts. Global css/scripts could be directly included in ``base.html`` to make them 
available to all child templates. (e.g. something general like ``jquery.js`` would go in base while something specific like ``jquery.form.js`` would go in
the child template)

.. note:: 

        Templates outside any subdirectory are considered harmful since they may interfere with templates from other applications.
        In general it is better to ``namespace`` your templates by putting them inside subdirectories.

        E.g.:

        * ``wiki/templates/base.html`` - Wrong!
        *  ``wiki/templates/wiki/base.html`` - Right.

        The reason being that templates from other apps extending ``base.html`` would find both ``wiki/templates/blog/base.html`` and
        ``wiki/templates/base.html``. Then you would be left at the mercy of precedence of ``TEMPLATE_LOADERS`` to get the blog base template
        and not the wiki base template.

        Of course, it can be useful if used correctly, but quite hard to debug if not.

At this point the user can submit a sign-up form. He will be sent an email with subject from ``wiki/templates/registration/activation_email_subject.text`` and
content from ``wiki/templates/registration/activation_email.txt``. Let's write these templates:

A nice base email template would be ``wiki/templates/registration/email.txt``:

.. literalinclude:: djen_project/wiki/templates/registration/email.txt
    :commit: 3a0af03
    :language: django

In ``wiki/templates/registration/activation_email_subject.txt``

.. literalinclude:: djen_project/wiki/templates/registration/activation_email_subject.txt
    :commit: 3a0af03
    :language: django

In ``wiki/templates/registration/activation_email.txt``

.. literalinclude:: djen_project/wiki/templates/registration/activation_email.txt
    :commit: 21404bb
    :language: django

Note the use of ``url`` templatetag to get the activation link. Also, the tag returns a relative url, so we use the ``site`` context variable
passed by the ``register`` view

.. note::

    If you have a mail server configured, well and good. If not, you could use gmail's smtp server by adding

    .. literalinclude:: djen_project/local_settings.py.example

    to ``local_settings.py``

At this point, a user should be able to sign-up, get the activation email, follow the activation link, complete registration and login.

All this by just writing down the tempalates. Amazing, isn't it?

Now you would have noticed that the logged in user is redirected to ``/accounts/profile``. We would next customize the wiki app and redirect
the user to the index page.

Article Management:
===================

This is similar to our last app (blog) in many ways. Significant changes would be:

* Allow any registered user to add/edit an article(instead of just the administrator).

* Allow ReST input instead of just plain text.

* Keep track of all edit sessions related to an article.

To demonstrate custom model managers, we would like to show only 'published' articles on the index page.

Let's write down the models:

.. literalinclude:: djen_project/wiki/models.py
    :commit: f8603b3

Most of the code should be familiar, some things that are new:

* The Article model will hold all articles, but only those with ``is_published`` set to ``True`` will be displayed on the front page.

* We have a defined a custom model manager called ``PublishedArticlesManager`` which is a queryset that only returns the published articles.

* Non-published articles would be used only for editing. So, we retain the default model manager by setting ``objects`` to ``models.Manager``

* Now, to fetch all articles, one would use ``Articles.objects.all``, while ``Artilces.published.all`` would return only published articles.

* A custom manager should subclass ``models.Manager`` and define the custom ``get_query_set`` property.

* The ``Edit`` class would hold an edit session by a registered user on an article.

* We see the use of ``verbose_name`` and ``help_text`` keyword arguments. By default, django will replace ``_`` with spaces and Capitalize
  the field name for the label. This can be overridden using ``verbose_name`` argument. ``help_text`` will be displayed below a field in 
  the rendered ``ModelForm``

Now, we will need urls similar to our previous app, plus we would need a url to see the article history.

.. literalinclude:: djen_project/wiki/urls.py
    :commit: 41bd9b3

Note that:

* We will use the object_list generic views for the article index page and detail page.

* We have to autofill the ``author`` to the logged-in user, so will write a custom view for that.

* Similarly, it would be better to write down custom views for edit article and article history pages.

Here are the forms we will need:

.. literalinclude:: djen_project/wiki/forms.py

Here:

* We are excluding ``author`` and ``slug`` which will be autofilled.

* We are inluding the ``summary`` field in ``Edit`` model only. The other fields (``article``, ``editor``, ``edited_on``) will be autofilled.


In our custom views:

.. literalinclude:: djen_project/wiki/views.py

* We are using the ``login_required`` decorator to only allow logged-in users to add/edit articles.

* ``get_object_or_404`` is a shortcut method which ``gets`` an object based on some criteria. While the ``get`` method throws an
  ``DoesNotExist`` when no match is found, this method automatically issues a ``404 Not Found`` response. This is useful when getting an
  object based on url parameters (``slug``, ``id`` etc.)

* ``redirect``, as we have seen, would issue a ``HttpResponseRedirect`` on the ``article's`` ``get_absolute_url`` property.

* ``edit_article`` includes two forms, one for the ``Article`` model and the other for the ``Edit`` model. We save both the forms one by one.

* As planned, the ``author`` field of ``article`` and ``editor``, ``article`` fields of ``Article`` and ``Edit`` respectively, are filled up
  before commiting ``save``.

* ``article_history`` view first checks if an article with the given ``slug`` exists. If yes, it forwards the request to the ``object_list`` generic
  view. We also pass the ``article`` from the generic view using ``extra_context``.

* Note the ``filter`` on the ``Edit`` model's queryset and the ``lookup`` on the related ``Article's`` slug.

