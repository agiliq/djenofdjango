from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^post/(?P<slug>[-\w]+)$', 
        'blog.views.view_post',
        name='blog_post_detail'),
    url(r'^add/post$', 
        'blog.views.add_post', 
        name='blog_add_post'),
)

