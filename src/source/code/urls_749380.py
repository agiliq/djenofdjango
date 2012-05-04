from django.conf.urls.defaults import *

from models import Paste

urlpatterns = patterns('',
    (r'$', 'django.views.generic.create_update.create_object', { 'model': Paste }),
)

