Chapter 3. Building a Pastebin.
--------------------------------

URL configuration - entry points:
=================================

We have already noticed urls.py in our project. This controls our website's
points of entry. All incoming urls will be matched with the regexes in the 
``urlpatterns`` and the view corresponding to the first match will get to handle
the request. A request url that does not match any urlconf entry will be 404'ed.

.. note:: brush up regexes in python from `python docs 
          <http://docs.python.org/library/re.html>`_ or 
          `diveintopython <http://diveintopython.org/regular_expressions/index.html>`_

As an example from our previous app:

.. literalinclude:: djen_project/urls.py

Now when we call http://127.0.0.1:8000/admin/ django matches that to the first regex. This urlconf
has included ``admin.urls`` which means that all further regex matches will be done with the ``admin.urls``
module. Once again, the first match will get to handle the request. You can think of this as 'mounting' the 
admin app at ``/admin/``. You are of course free to change the 'mount point' to anything else you like.

A typical urlconf entry looks like this::

    (r'<regex>', <view_function>, <arg_dict>),

``regex`` is any valid python regex that has to be processed. This would be absolute in the project
urls.py and relative to the mount point in an app's urls.py

``view_function`` is a function that corresponds to this url. The function **must** return a ``HttpResponse``
object. Usually, shortcuts such as ``render_to_response``, are used though. More about views later.

``arg_dict`` is an optional dict of arguments that will be passed to the ``view_function``. In addition, options
can be declared from the url regex too. For example::

    (r'^object/?P<object_id>(\d+)$', 'objects.views.get_object'),

will match all urls having an integer after ``object/``. Also, the value will be passed as ``object_id`` to the 
``get_object`` function.

Named urls:
+++++++++++

Usually, we would want an easier way to remember the urls so that we could refer them in views or templates.
We could *name* our urls by using the ``url`` constructor. For example::

    url(r'^welcome/$', 'app.views.welcome', name='welcome'),

This line is similar to the previous urls, but we have an option of passing a ``name`` argument. 

To get back the url from its name, django provides:

* ``django.core.urlresolvers.reverse`` function for use in views

* ``url`` templatetag for use in templates

We will see how to use the templatetag in our templates.

.. note:: Also see http://agiliq.com/books/djangodesignpatterns/urls.html#naming-urls

Grouped urls:
++++++++++++++

Sometimes, we would want to group together logically related urls. Or just avoid writing the full function path
over and over. We can do this by putting the common path to the view function in the first argument of
urlpatterns::

        urlpatterns = patterns('',
            (r'^$', 'django.views.generic.create_update.create_object', { 'model': Paste }),
        )

and::

        urlpatterns = patterns('django.views.generic.create_update',
            (r'^$', 'create_object', { 'model': Paste }),
        )

are equivalent.

Templates - skeletons of our website:
======================================

You must be wondering where all those pages came from, since we have not touched
any html yet. Well, since we used the admin app, we were able to rely on the admin
templates supplied with django.

A template is a structure of webpage that will be *rendered* using a *context* and returned as response if
you want it to. A ``django.template.Template`` object can be rendered using the ``render`` method.

Normally templates are html files with some extra django content, such as templatetags and variables. Note that our
templates need not be publicly accessible(in fact they shouldn't be) from a webserver. They are not meant to be displayed
directly; django will process them based on the request, context etc and respond with the rendered templates.

In case you want a template to be directly accessible (e.g. static html files), you could use the ``django.views.generic.simple.direct_to_template`` 
generic view.

Template Loaders:
+++++++++++++++++

Django will usually look for templates in ``TEMPLATE_DIRS``  of settings.py and inside ``templates`` directory of each app.
This is because of the ``TEMPLATE_LOADERS`` in the default settings.py::

    # List of callables that know how to import templates from various sources.
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )

These functions fetch the template based on a given template path. To let django locate your ``hello_world.html``
you would have to place it in ``<app>/templates`` or place it in any directory and set the ``TEMPLATE_DIRS``::

    TEMPLATE_DIRS = (
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    )


to the absolute path of that directory.

Context:
++++++++

A context is a dict that will be used to render a page from a template. All context keys are valid template
variables.

To display a user name in your template, suppose you provide the ``username`` in your context, you could do:

.. sourcecode:: django

    Hello {{ username }}

When this template is rendered using (e.g. using ``render_to_response``), ``username`` will be replaced with its value

You can pass any variable to the context, so you can call a dict's key, or an objects property. However you cannot pass
any arguments to the property.

For example:

.. sourcecode:: django

    Hello {{ user.username }}

can be used to get ``user['username']`` or ``user.username``

Similarly:

.. sourcecode:: django

    <a hef="{{ user.get_absolute_url }}">{{ user.username }}</a>

can be used to get ``user.get_absolute_url()``

Templatetags:
+++++++++++++

Templatetags are helpers to the template. Suppose you have an ``iterable`` with a list of objects in your context:

.. sourcecode:: django

    {% for object in objects %}
        {{ object }}
    {% endfor %}

would render them. If this is a html template, we would prefer:

.. sourcecode:: django

    {% if objects %}
    <ul>
        {% for object in objects %}
            <li>
                {{ object }}
            </li>
        {% endfor %}
    </ul>
    {% endif %}

which would render the objects in html unordered list.

Note that ``{% if %}`` ``{% for %}`` ``{% endif %}`` ``{% endfor %}`` are all built-in templatetags.
If and for behave very much like their python counterparts.

Common templatetags and template inheritance:
++++++++++++++++++++++++++++++++++++++++++++++

Some templatetags we will use in our application:

* ``url`` 
  
This templatetag takes a named url or view function and renders the url as found by ``reverse``

  For example:
  
.. sourcecode:: django

    <a href="{% url pastebin_paste_list %}">View All</a>

would output

.. sourcecode:: html

    <a href="/pastebin/pastes/">View All</a>

It also takes arguments:

.. sourcecode:: django

    <a href="{% url pastebin_paste_detail paste.id  %}">{{ paste }}</a>

would output

.. sourcecode:: html

    <a href="/pastebin/paste/9">Sample Paste</a>

.. note:: You must make sure the correct urlconf entry for the give url exists. If the url entry
          does not exist, or the number of arguments does not match, this templatetag will raise a 
          ``NoReverseMatch`` exception.


* ``csrf_token`` 

  This is a security related tag used in forms to prevent cross site request forgery.

* ``include <template>``

  This will simply include any file that can be found by the ``TEMPLATE_LOADERS`` where it is called

* ``extends <template>``

  This will extend another template and provides template inheritance. You can have a ``base`` template and
  have other specific template extend the ``base`` template.

* ``block`` and ``endblock``

  ``blocks`` are used to customize the ``base`` page from a ``child`` page. If the ``base`` page defines a block called
   ``head``, the child page can override that block with its own contents.

* ``load``

  This is used to load custom templatetags. More about writing and using custom templatetags later.

We will see later how to add custom templatetags.

Filters:
++++++++

Filters are simple functions which operate on a template variable and manipulate them.

For example in our previous template:

.. sourcecode:: django

    Hello {{ username|capfirst }}

Here ``capfirst`` is a filter that will capitalize the first char our ``username``


.. note:: Reference of built-in templatetags and filters:
          http://docs.djangoproject.com/en/1.2/ref/templates/builtins/

Templates are not meant for programming:
++++++++++++++++++++++++++++++++++++++++

One of the core django philosophy is that templates are meant for rendering the context and
optionally making a few aesthetic changes only. Templates should not be used for handling 
complex queries or operations. This is also useful to keep the programming and designing aspects
of the website separate. Template language should be easy enough to be written by designers.

Generic views - commonly used views:
====================================

Views:
++++++

Views are just functions which take the ``HttpRequest`` object,  and some optional arguments,
then do some work and return a ``HttpResponse`` page. Use ``HttpResponseRedirect`` to redirect
to some other ``url`` or ``HttpResponseForbidden`` to return a ``403 Forbidden`` response.

By convention, all of an app's views would be written in <app>/views.py

A simple example to return "Hello World!" string response:

.. sourcecode:: python

    from django.http import HttpResponse

    def hello_world(request):
        return HttpResponse("Hello World!")

To render a template to response one would do:

.. sourcecode:: python

    from django.http import HttpResponse
    from django.template import Context, loader

    def hello_world(request):
        template = loader.get_template("hello_world.html")
        context = Context({"username": "Monty Python"})
        return HttpResponse(template.render(context))

But there's a simpler way:

.. sourcecode:: python

    from django.shortcuts import render_to_response

    def hello_world(request):
        return render_to_response("hello_world.html", { "username": "Monty Python" })


Generic Views:
+++++++++++++++

Generic views are commonly used view patterns that are shipped with django to make
common operations such a list, detail, create, update delete easy. To do these operations,
we need not even write any views, we can use generic views by passing the proper arguments.

We will be using the ``create_update`` and ``list_detail`` generic views in this chapter

.. note:: reference: http://docs.djangoproject.com/en/dev/ref/generic-views/

``create_update.create_object``
+++++++++++++++++++++++++++++++

The ``create_object`` generic view is used to render the object creation page with the
object form, perform form validation and save valid objects to the database.

It takes a ``model`` argument which is the model that has to be created. By default, it renders
to template with the name ``<app>/<model>_form.html``. This can be changed using the ``template_name``
argument. (this applies to all generic views listed here)

The view provides ``form`` variable in the context. This is the generated ModelForm of the ``model``.


``create_update.update_object``
+++++++++++++++++++++++++++++++

In addition to the ``model`` argument, the ``update_object`` generic view also requires a ``object_id``
argument which is the ``id`` of the object to be updated. This also renders to ``<app>/<model>_form.html`` template.

In addition to the ``form`` variable, this view also provides the ``object`` that is being edited to the context.


``create_update.delete_object``
+++++++++++++++++++++++++++++++

In addition to both the above arguments, this view also requires a ``post_delete_redirect`` argument
which is the url to redirect after deleting. If called using the ``GET`` method, this view will
redirect to ``<app>/<model>_confirm_delete.html`` template. To actually delete the object, this
view needs to be called using the ``POST`` method. This is in accordance with the best practices that
``GET`` requests should not modify any data.

``list_detail.object_list``
++++++++++++++++++++++++++++

The ``object_list`` generic view shows the list of the ``queryset``, where ``queryset`` is the 
queryset containing the objects we want to list.

It renders the ``<app>/<model>_list.html`` template and provides ``object_list`` context
variable by default.

``list_detail.object_detail``
+++++++++++++++++++++++++++++

The ``object_detail`` generic view show details about a particular object. It takes the ``queryset`` to fetch
the ``object_id`` from and returns ``object`` in the context.

It renders to ``<app>/<model>_detail.html`` by default.

Designing a pastebin app:
=========================

In this chapter we will be designing a simple pastebin. Our pastebin will be able to

    * Allow users to paste some text

    * Allow users to edit or delete the text

    * Allow users to view all texts

    * Clean up texts older than a day

Some 'views' that the user will see are

    * A list view of all recent texts

    * A detail view of any selected text

    * An entry/edit form for a text

    * A view to delete a text

Since the list and detail views are fairly common in most apps,
django ships with a set of 'generic views' that can be used in
our app. We would be particularly interested in the following generic
views

    * ``django.views.generic.create_update.create_object``

    * ``django.views.generic.create_update.update_object``

    * ``django.views.generic.create_update.delete_object``

    * ``django.views.generic.list_detail.object_list``

    * ``django.views.generic.list_detail.object_detail``

Our work flow for this app would be

    * sketch the models

    * route urls to generic views

    * use generic views with our models

    * write the templates to use generic views

So let's dive in:

Sketch the models:
==================

We have only one object to store to the database which is 
the text pasted by the user. Let's call this Paste.

Some things our Paste model would need to handle are

    * Text pasted by the user

    * Optional file name

    * Created time

    * Updated time

The time fields would be useful for getting 'latest' or 'recently updated'
pastes.

So let's get started::

    python manage.py startapp pastebin

In pastebin/models.py

.. literalinclude:: code/models_a9ffd8.py

.. note::

    * auto_now_add automatically adds current time to the created_on
      field when an object is added.

    * auto_now is similar to the above, but it adds the current time to
      the updated_on field each time an object is saved.

    * the id field is primary key which is autocreated by django. Since
      name is optional, we fall back to the id which is guaranteed.

Adding our app to the project

.. literalinclude:: djen_project/settings.py
    :lines: 86-96

And syncdb'ing::

    python manage.py syncdb

which returns::

    Creating table pastebin_paste
    No fixtures found.

There, we have our pastebin models ready.

Configuring urls:
=================

We have already seen how to include the admin urls in urls.py. But now, we want to have
our app take control of the urls and direct them to generic views. Here's how

Let's create urls.py in our app. Now our pastebin/urls.py should look like

.. literalinclude:: code/urls_749380.py

Notes:

* Each urlpatterns line is a mapping of urls to views

  ``(r'^$', 'django.views.generic.create_update.create_object', { 'model': Paste }),``

* Here the url is ``r'^$'`` which is a regular expression that will be matched with the incoming request.
  If a match is found, the request is forwarded to the corresponding view.

* The third value is the arguments passed to the ``create_object`` view. The view will use the ``model``
  argument to generate a form and save it to the database. In our case, this is the ``Paste`` model

Let's tell the project to include our app's urls

.. literalinclude:: djen_project/urls.py

Now django knows to forward urls starting with ``/pastebin`` to the pastebin app. All urls relative to this url
will be handled by the pastebin app. That's great for reusability.

If you try to open http://127.0.0.1/pastebin at this point, you will be greeted with a TemplateDoesNotExist error.
If you observe, the error message says that django cannot find ``pastebin/paste_form.html``. Usually getting this error means that
django was not able to find that file. 

The default template used by create_object is '<app>/<model>_form.html'. In our case this would be ``pastebin/paste_form.html``.

Let's create this template. In ``pastebin/templates/pastebin/paste_form.html``:

.. literalinclude:: djen_project/pastebin/templates/pastebin/paste_form.html
    :language: django

.. TODO::

    This is not the right place to discuss templates, introduce templates, context, RequestContext in first chapter

Observe that:

* the create_object generic view has provided a ``form`` context variable.

* the form has been autogenerated by django's forms library by using the ``Paste`` model

* to display the form, all you have to do is render the ``form`` variable

* form has a method ``as_table`` that will render it as table, other options are ``as_p``, ``as_ul``
  for enclosing the form in ``<p>`` and ``<ul>`` tags respectively

* form does not output the form tags or the submit button, so we will have to write them down
  in the template

* you need to include ``csrf_token`` tag in every form posted to a local view. Django uses this to prevent
  cross site request forgery

* the generated form includes validation based on the model fields

Now, we need a page to redirect successful submissions to. We can use the detail view page of a paste here.

For this, we will use the ``django.views.generic.list_detail.object_detail`` generic view:

.. literalinclude:: code/urls_5013af.py

Using this generic view we will be able to display the details about the paste object with a given id. Note that:

* object_id and queryset are the arguments passed to object_detail view

* we are naming this view using the url constructor and passing the ``name`` argument. This name can be referred to
  from views or templates and helps in keeping this DRY.

* the object_detail view will render the ``pastebin/paste_detail.html`` template by default. We need to write down this
  template for this view to work.

In ``pastebin/templates/pastebin/paste_detail.html``:

.. literalinclude:: code/paste_detail_c5f0c2.html
    :language: django

Now, that we have a create view and a detail view, we just need to glue them together. We can do this in two ways:

* pass the ``post_save_redirect`` argument in ``create_object`` view

* set the ``get_absolute_url`` property of our Paste model to its detail view. ``create_object`` view will call the object's
  ``get_absolute_url`` by default

I would choose the latter because it is more general. To do this, change your Paste model and add the get_absolute_url property:

.. literalinclude:: code/models_c0c759.py

Note that:

* We could have returned ``'/pastebin/paste/%s' %(self.id)'`` but it would mean defining the same url twice and it violates the DRY principle.
  Using the ``models.permalink`` decorator, we can tell django to call the url named ``pastebin_paste_detail`` with the parameter ``id``

And so, we are ready with the create object and object detail views. Try submitting any pastes and you should be redirected to the details of 
your paste.

Now, on to our next generic view, which is object list:

.. literalinclude:: code/urls_dee14b.py

This is simpler than the detail view, since it does not take any arguments in the url. The default template for this view is ``pastebin/paste_list.html``
so let's fill that up with:

.. literalinclude:: code/paste_list_dee14b.html
    :language: django

Note that

* We have used the ``url`` template tag and passed our named view i.e. ``pastebin_paste_detail`` to get the url to a specific paste

Similarly, our update and delete generic views would look like:

.. literalinclude:: code/urls_17c506.py

Note that the ``delete_object`` generic view requires an argument called ``post_delete_redirect`` which will be used to redirect the user
after deleting the object.

We have used update_object, delete_object for the update/delete views respectively. Let's link these urls from the detail page:

.. literalinclude:: code/paste_detail_17c506.html
    :language: django

Note that the delete view redirects to a confirmation page whose template name is ``paste_confirm_delete.html`` if called using GET method.
Once in the confirmation page, we need need to call the same view with a POST method. The view will delete the object and pass a message using 
the messages framework.

.. literalinclude:: code/paste_confirm_delete_17c506.html
    :language: django

Let's handle the message and display it in the redirected page.

.. literalinclude:: code/paste_list_17c506.html
    :language: django

While we are at it, Let's also include the messages in paste detail page, where create/update view sends the messages:

.. literalinclude:: djen_project/pastebin/templates/pastebin/paste_detail.html
    :language: django

So we now have pages to create, update, delete and view all pastes.

Now, for better maintenance, we would like to delete all pastes that have not been updated in a day using an script.
We will use django's custom management scripts for this.

Writing custom management scripts:
===================================

Just like other manage.py subcommands such as ``syncdb``, ``shell``, ``startapp`` and ``runserver``, we can have custom subcommands to
help us maintain the app.

For our subcommand to be registered with manage.py, we need the following structure in our app::

    .
    |-- __init__.py
    |-- management
    |   |-- commands
    |   |   `-- __init__.py
    |   `-- __init__.py
    |-- models.py
    |-- templates
    |-- tests.py
    |-- urls.py
    `-- views.py

All scripts inside ``management/commands/`` will be used as custom subcommands. Let's create ``delete_old.py`` subcommand:

.. literalinclude:: djen_project/pastebin/management/commands/delete_old.py

Here:

* We subclass either of the ``NoArgsCommand``, ``LabelCommand`` or ``AppCommand`` from ``django.core.management.base``. ``NoArgsCommand``
  suits our need because we dont need to pass any arguments to this subcommand.

* ``handle_noargs`` will be called when the script runs. This would be ``handle`` for other Command types.

* We have used the ``lte`` lookup on ``updated_on`` field to get all posts older than a day. Then we delete them using ``delete`` method
  on the queryset.

You can test if the subcommand works by doing::

    python manage.py delete_old

Now we can configure this script to run daily using cronjob or something similar.

