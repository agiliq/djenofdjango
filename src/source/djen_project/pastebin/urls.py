from django.conf.urls.defaults import *

from models import Paste

urlpatterns = patterns('',
    (r'$', 'django.views.generic.list_detail.object_list', { 'queryset': Paste.objects.all() }),
)

