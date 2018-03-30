from django.urls import re_path, include
from .views import view_post, add_post, PostMonthArchiveView, PostWeekArchiveView


urlpatterns = [
    re_path(r'^post/(?P<slug>[-\w]+)$', view_post, name='blog_post_detail'),
    re_path(r'^add/post$', add_post, name='blog_add_post'),
    re_path(r'^archive/<int:year>/month/<int:month>$', PostMonthArchiveView.as_view(month_format='%m'), name='blog_archive_month',),
    re_path(r'^archive/<int:year>/week/<int:week>$', PostWeekArchiveView.as_view(), name='blog_archive_week'),
        ]

