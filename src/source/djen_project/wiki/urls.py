from django.conf.urls.defaults import *

from models import Article

urlpatterns = patterns('',
    url(r'^article/(?P<slug>[-\w]+)$', 
        'django.views.generic.list_detail.object_detail',
        {
            'queryset': Article.published.all(),
        },
        name='wiki_article_detail'),
    url(r'^add/post$', 
        'blog.views.add_post', 
        name='blog_add_post'),
    url(r'^archive/month/(?P<year>\d+)/(?P<month>\w+)$',
        'django.views.generic.date_based.archive_month',
        {
            'queryset': Post.objects.all(), 
            'date_field': 'created_on',
        },
        name='blog_archive_month',
       ),
    url(r'^archive/week/(?P<year>\d+)/(?P<week>\d+)$',
        'django.views.generic.date_based.archive_week',
        {
            'queryset': Post.objects.all(), 
            'date_field': 'created_on',
        },
        name='blog_archive_week',
       ),
)

    url(r'^paste/(?P<object_id>\d+)$', 'django.views.generic.list_detail.object_detail', { 'queryset': Paste.objects.all() }, name='pastebin_paste_detail'),
