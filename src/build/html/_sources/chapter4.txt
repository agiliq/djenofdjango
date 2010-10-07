Chapter 4. Building a Blog
----------------------------
(Topics introduced: Authentication, Session management, NewForms, Generating simple RSS feeds. Date based generic views.)
 
Diving in. [Code listing]
 
Authentication. [In chapter 2, all views were managed by Admin, so we did not need to handle authentication. In chapter 3, all views would be public, so no authentication was needed. In this chapter we need to restrict access to only logged in user, so we introduce it here.]
  Using django.contrib.auth
  Using login_required decorator to restrict access to logged in users.
  Using request.user in views, for finer control over views.
  Using context processors to use logged in users in templates.

Session Management. [So once user has commented, their name/email information is stored.]  
  The machinery behind sessions framework.
  Using cookies.
  Using session to abstract handling cookies.
  
Newforms. [Comment, Post, Settings form]
  Using newforms.
  Using model form to auto generate forms for model.
  Creating complex forms programatically. (Instead of defining them.)
  
Generating RSS feeds.
  Using django.contrib.syndication to generate feeds for the Blog.
  
Using date based generic views to generate monthly and weekly archives for the blog.

