Chapter 5. Building a Wiki
-----------------------------
...
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

* Article Management (CRUD)

* Markup support (ReST)

* Audit trail for article

* Revision history

