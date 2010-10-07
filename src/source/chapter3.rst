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

``view_function`` is a function that corresponds to this url. The funtion **must** return a ``HttpResponse``
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
you want it to.

Normally templates are html files with some extra django content, such as templatetags and variables.

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
We will see later how to add custom templatetags.

Filters:
++++++++

Filters are simple functions which operate on a template variable and manipulate them.

For example in our previous template:

.. sourcecode:: django

    Hello {{ username|capfirst }}

Here ``capfirst`` is a filter that will capitalize the first char our ``username``

Templates are not meant for programming:
++++++++++++++++++++++++++++++++++++++++

One of the core django philosphy is that templates are meant for rendering the context and
optionally making a few aesthetic changes only. Templates should not be used for handling 
complex queries or operations. This is also useful to keep the programming and designing aspects
of the website separate. Template language should be easy enough to be written by designers.

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

    * ``django.views.generic.list_detail.object_list``

    * ``django.views.generic.list_detail.object_detail``

Our workflow for this app would be

    * sketch the models

    * route urls to generic views

    * use generic views with our models

    * write the templates to use generic views

So lets dive in:

Sketch the models:
==================

We have only one object to store to the database which is 
the text pasted by the user. Lets call this Paste.

Some things our Paste model would need to handle are

    * Text pasted by the user

    * Optional file name

    * Created time

    * Updated time

The time fields would be useful for getting 'latest' or 'recently updated'
pastes.

So lets get started::

    python manage.py startapp pastebin

In pastebin/models.py

.. literalinclude:: djen_project/pastebin/models.py
    :commit: a9ffd8d6d733fc62afb7

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

Lets create urls.py in our app. Now our pastebin/urls.py should look like

.. literalinclude:: djen_project/pastebin/urls.py
    :commit: 749380e3986665022283

Notes:

* Each urlpatterns line is a mapping of urls to views

  ``(r'^$', 'django.views.generic.create_update.create_object', { 'model': Paste }),``

* Here the url is r'^$' which is a regular expression that will be matched with the incoming request.
  If a match is found, the request is forwarded to the corresponding view.

* The third value is the arguments passed to the create_object view. The view will use the ``model``
  argument to generate a form and save it to the database. In our case, this is the ``Paste`` model

Lets tell the project to include our app's urls

.. literalinclude:: djen_project/urls.py

Now django knows to forward urls starting with ``/pastebin`` to the pastebin app. All urls relative to this url
will be handled by the pastebin app. That's great for reusability.

If you try to open http://127.0.0.1/pastebin at this point, you will be greeted with a TemplateDoesNotExist error.
If you observe, it says that django cannot find ``pastebin/paste_form.html``. Usually getting this error means that
django was not able to find that file. 

Django will usually look for templates in TEMPLATE_DIRS  of settings.py and inside ``templates`` directory of each app.

The default template used by create_object is '<app>/<model>_form.html'. In our case this would be ``pastebin/paste_form.html``.

Lets create this template. In ``pastebin/templates/pastebin/paste_form.html``:

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

.. literalinclude:: djen_project/pastebin/urls.py
    :commit: 5013afc980dd97950b5c

Using this generic view we will be able to display the details about the paste object with a given id. Note that:

* object_id and queryset are the arguments passed to object_detail view

* we are naming this view using the url constructor and passing the ``name`` argument. This name can be referred to
  from views or templates and helps in keeping this DRY.

* the object_detail view will render the ``pastebin/paste_detail.html`` template by default. We need to write down this
  template for this view to work.

In ``pastebin/templates/pastebin/paste_detail.html``:

.. literalinclude:: djen_project/pastebin/templates/pastebin/paste_detail.html
    :commit: c5f0c2d3a37c15eb7ee6
    :language: django

Now, that we have a create view and a detail view, we just need to glue them together. We can do this in two ways:

* pass the ``post_save_redirect`` argument in ``create_object`` view

* set the ``get_absolute_url`` property of our Paste model to its detail view. ``create_object`` view will call the object's
  ``get_absolute_url`` by default

I would choose the latter because it is more general. To do this, change your Paste model and add the get_absolute_url property:

.. literalinclude:: djen_project/pastebin/models.py
    :commit: c0c759bd1cc6d2596c8b

Note that:

* We could have returned ``'/pastebin/paste/%s' %(self.id)'`` but it would mean defining the same url twice and it violates the DRY principle.
  Using the ``models.permalink`` decorator, we can tell django to call the url named ``pastebin_paste_detail`` with the parameter ``id``

And so, we are ready with the create object and object detail views. Try submitting any pastes and you should be redirected to the details of 
your paste.

Now, on to our next generic view, which is object list:

.. literalinclude:: djen_project/pastebin/urls.py
    :commit: dee14b3013b9f84bfd18

This is simpler than the detail view, since it does not take any arguments in the url. The default template for this view is ``pastebin/paste_list.html``
so lets fill that up with:

.. literalinclude:: djen_project/pastebin/templates/pastebin/paste_list.html
    :commit: dee14b3013b9f84bfd18
    :language: django

Note that

* We have used the ``url`` template tag and passed our named view i.e. ``pastebin_paste_detail`` to get the url to a specific paste

Similarly, our update and delete generic views would look like:

.. literalinclude:: djen_project/pastebin/urls.py
    :commit: 17c5062a18dc4e9edfbc

Note that the ``delete_object`` generic view requires an argument called ``post_delete_redirect`` which will be used to redirect the user
after deleting the object.

We have used update_object, delete_object for the update/delete views respectively. Lets link these urls from the detail page:

.. literalinclude:: djen_project/pastebin/templates/pastebin/paste_detail.html
    :commit: 17c5062a18dc4e9edfbc
    :language: django

Note that the delete view redirects to a confirmation page whose template name is ``paste_confirm_delete.html`` if called using GET method.
Once in the confirmation page, we need need to call the same view with a POST method. The view will delete the object a pass a message using 
the messages framework.

.. literalinclude:: djen_project/pastebin/templates/pastebin/paste_confirm_delete.html
    :commit: 17c5062a18dc4e9edfbc
    :language: django

Let's handle the message and display it in the redirected page.

.. literalinclude:: djen_project/pastebin/templates/pastebin/paste_list.html
    :commit: 17c5062a18dc4e9edfbc
    :language: django

While we are at it, lets also include the messages in paste detail page, where create/update view sends the messages:

.. literalinclude:: djen_project/pastebin/templates/pastebin/paste_detail.html
    :language: django

So we now have pages to create, update, delete and view all pastes.

Now, for better maintenance, we would like to delete all pastes that have not been updated in a day using an script.
We will use django's custom management scripts for this.

Writing custom management scrips:
=================================

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

All scripts inside ``management/commands/`` will be used as custom subcommands. Lets create ``delete_old.py`` subcommand:

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

