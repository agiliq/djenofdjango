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

    * ``django.views.generic.object_list``

    * ``django.views.generic.list_detail``

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

Notes:

* Each urlpatterns line is a mapping of urls to views

  ``(r'$', 'django.views.generic.list_detail.object_list', {'queryset': Paste.objects.all()}),``

* Here the url is r'$' which is a regular expression that will be matched with the incoming request.
  If a match is found, the request is forwarded to the corresponding view.

* The view is passed as a string representing a function present in PYTHONPATH. You can also
  specify where to look for the view by providing the first argument of ``patterns``. If so,
  you only need to pass the function path relative to the given path. For example::

        urlpatterns = patterns('',
            (r'$', 'django.views.generic.list_detail.object_list', { 'queryset': Paste.objects.all() }),
        )

  and::

        urlpatterns = patterns('django.views.generic.list_detail',
            (r'$', 'object_list', { 'queryset': Paste.objects.all() }),
        )

  are equivivalent.

Lets tell the project to include our app's urls

.. literalinclude:: djen_project/urls.py

ow django knows to forward urls starting with ``/pastebin`` to the pastebin app. All urls relative to this url
will be handled by the pastebin app. That's great for reusability.

If you try to open http://127.0.0.1/pastebin at this point, you will be greeted with a TemplateDoesNotExist error.
If you observe, it says that django cannot find ``pastebin/paste_list.html``. Usually getting this error means that
django was not able to find that file. Don't worry, this just needs one more step.

Django will usually look for templates in TEMPLATE_DIRS  of settings.py and inside ``templates`` directory of each app.

The default template used by object_list is '<app>/<model>_list.html'. In our case this would be ``pastebin/paste_list.html``.

Lets create this template. In ``pastebin/templates/pastebin/paste_list.html``:


