from django.conf.urls.defaults import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from models import Paste

urlpatterns = patterns('',
    url(r'^$', CreateView.as_view(model=Paste), name='pastebin_paste_create'),
    url(r'^paste/edit/(?P<pk>\d+)$', UpdateView.as_view(model=Paste), name='pastebin_paste_edit'),
    url(r'^paste/delete/(?P<pk>\d+)$', DeleteView.as_view(model=Paste, success_url='/pastebin/pastes'), name='pastebin_paste_delete'),
    url(r'^paste/(?P<object_id>\d+)$', 'django.views.generic.list_detail.object_detail', { 'queryset': Paste.objects.all() }, name='pastebin_paste_detail'),
    url(r'^pastes/$', 'django.views.generic.list_detail.object_list', { 'queryset': Paste.objects.all() }, name='pastebin_paste_list'),
)

