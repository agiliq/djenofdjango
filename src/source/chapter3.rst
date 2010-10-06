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
    :lines: 1-14

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
    :lines: 1-6, 8-9

Notes:

* Each urlpatterns line is a mapping of urls to views

  ``(r'^$', 'django.views.generic.create_update.create_object', { 'model': Paste }),``

* Here the url is r'^$' which is a regular expression that will be matched with the incoming request.
  If a match is found, the request is forwarded to the corresponding view.

* The third value is the arguments passed to the create_object view. The view will use the ``model``
  argument to generate a form and save it to the database. In our case, this is the ``Paste`` model

* The view is passed as a string representing a function present in PYTHONPATH. You can also
  specify where to look for the view by providing the first argument of ``patterns``. If so,
  you only need to pass the function path relative to the given path. For example::

        urlpatterns = patterns('',
            (r'^$', 'django.views.generic.create_update.create_object', { 'model': Paste }),
        )

  and::

        urlpatterns = patterns('django.views.generic.create_update',
            (r'^$', 'create_object', { 'model': Paste }),
        )

  are equivalent.

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

Using this generic view we will be able to display the details about the paste object with a given id. Note that:

* object_id and queryset are the arguments passed to object_detail view

* we are naming this view using the url constructor and passing the ``name`` argument. This name can be referred to
  from views or templates and helps in keeping this DRY.

* the object_detail view will render the ``pastebin/paste_detail.html`` template by default. We need to write down this
  template for this view to work.

In ``pastebin/templates/pastebin/paste_detail.html``:

.. literalinclude:: djen_project/pastebin/templates/pastebin/paste_detail.html
    :language: django

Now, that we have a create view and a detail view, we just need to glue them together. We can do this in two ways:

* pass the ``post_save_redirect`` argument in ``create_object`` view

* set the ``get_absolute_url`` property of our Paste model to its detail view. ``create_object`` view will call the object's
  ``get_absolute_url`` by default

I would choose the latter because it is more general. To do this, change your Paste model and add the get_absolute_url property:

.. literalinclude:: djen_project/pastebin/models.py

Note that:

* We could have returned ``'/pastebin/paste/%s' %(self.id)'`` but it would mean defining the same url twice and it violates the DRY principle.
  Using the ``models.permalink`` decorator, we can tell django to call the url named ``pastebin_paste_detail`` with the parameter ``id``

And so, we are ready with the create object and object detail views. Try submitting any pastes and you should be redirected to the details of 
your paste.

Now, on to our next generic view, which is object list:

.. literalinclude:: djen_project/pastebin/urls.py

This is simpler than the detail view, since it does not take any arguments in the url. The default template for this view is ``pastebin/paste_list.html``
so lets fill that up with:

.. literalinclude:: djen_project/pastebin/templates/pastebin/paste_list.html
    :language: django

Note that

* We have used the ``url`` template tag and passed our named view i.e. ``pastebin_paste_detail`` to get the url to a specific paste

Similarly, our update and delete generic views would look like:

.. literalinclude:: djen_project/pastebin/urls.py

Note that the ``delete_object`` generic view requires an argument called ``post_delete_redirect`` which will be used to redirect the user
after deleting the object.

We have used update_object, delete_object for the update/delete views respectively. Lets link these urls from the detail page:

.. literalinclude:: djen_project/pastebin/templates/pastebin/paste_detail.html
    :language: django

Note that the delete view redirects to a confirmation page whose template name is ``paste_confirm_delete.html`` if called using GET method.
Once in the confirmation page, we need need to call the same view with a POST method. The view will delete the object a pass a message using 
the messages framework.

.. literalinclude:: djen_project/pastebin/templates/pastebin/paste_confirm_delete.html
    :language: django

Let's handle the message and display it in the redirected page.

.. literalinclude:: djen_project/pastebin/templates/pastebin/paste_list.html
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

