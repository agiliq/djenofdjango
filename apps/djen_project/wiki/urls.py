from django.urls import re_path, include
from .views import add_article, edit_article, article_history, ArticleList, ArticleDetail

urlpatterns = [
    re_path(r'^$', ArticleList.as_view(), name='wiki_article_index'),
    re_path(r'^article/(?P<slug>[-\w]+)$',ArticleDetail.as_view(),name='wiki_article_detail'),
    re_path(r'^history/(?P<slug>[-\w]+)$', article_history, name='wiki_article_history'),
    re_path(r'^add/article$', add_article, name='wiki_article_add'),
    re_path(r'^edit/article/(?P<slug>[-\w]+)$', edit_article, name='wiki_article_edit'),
]