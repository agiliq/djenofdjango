from django.conf.urls.defaults import *

from models import Post

urlpatterns = patterns('',
    url(r'^post/(?P<slug>[-\w]+)$', 
        'django.views.generic.list_detail.object_detail', 
        {
            'queryset': Post.objects.all(),
            'template_name': 'blog/blog_post.html',
            'template_object_name': 'post',
        }, 
        name='blog_post_detail'),
    url(r'^add/post$', 
        'blog.views.add_post', 
        name='blog_add_post'),
)

