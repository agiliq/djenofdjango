from django.urls import path, include
from .views import view_post, add_post, PostMonthArchiveView, PostWeekArchiveView


urlpatterns = [
    path('post/<str:slug>', view_post, name='blog_post_detail'),
    path('add/post', add_post, name='blog_add_post'),
    path('archive/<int:year>/month/<int:month>', PostMonthArchiveView.as_view(month_format='%m'), name='blog_archive_month',),
    path('archive/<int:year>/week/<int:week>', PostWeekArchiveView.as_view(), name='blog_archive_week'),
        ]

