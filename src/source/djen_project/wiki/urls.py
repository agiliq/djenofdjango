from django.conf.urls.defaults import *

from models import Article

urlpatterns = patterns('',
    url(r'^article/(?P<slug>[-\w]+)$', 
        'django.views.generic.list_detail.object_detail',
        {
            'queryset': Article.objects.all(),
        },
        name='wiki_article_detail'),
    url(r'^add/article$',
        'wiki.views.add_article',
        name='wiki_article_add'),
    url(r'^edit/article/(?P<slug>[-\w]+)$',
        'wiki.views.edit_article',
        name='wiki_article_edit'),
)

