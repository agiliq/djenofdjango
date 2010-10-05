from django.conf.urls.defaults import *

from models import Paste

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.create_update.create_object', { 'model': Paste }, name='pastebin_paste_create'),
    url(r'^paste/(?P<object_id>\d+)$', 'django.views.generic.list_detail.object_detail', { 'queryset': Paste.objects.all() }, name='pastebin_paste_detail'),
    url(r'^pastes/$', 'django.views.generic.list_detail.object_list', { 'queryset': Paste.objects.all() }, name='pastebin_paste_list'),
)

