from django.conf.urls.defaults import *

from models import Paste

urlpatterns = patterns('django.views.generic.list_detail',
    (r'$', 'object_list', { 'queryset': Paste.objects.all() }),
)

