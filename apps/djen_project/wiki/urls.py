from django.urls import path, include
from .views import add_article, edit_article, article_history, ArticleList, ArticleDetail

urlpatterns = [
    path('', ArticleList.as_view(), name='wiki_article_index'),
    path('article/<str:slug>',ArticleDetail.as_view(),name='wiki_article_detail'),
    path('history/<str:slug>', article_history, name='wiki_article_history'),
    path('add/article', add_article, name='wiki_article_add'),
    path('edit/article/<str:slug>', edit_article, name='wiki_article_edit'),
]