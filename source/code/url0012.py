from django.urls import re_path
from .views import PasteDetail, PasteCreate

urlpatterns = [
    re_path(r'', PasteCreate.as_view(), name='create'),
    re_path(r'^paste/(?P<pk>\d+)$', PasteDetail.as_view(), name='pastebin_paste_detail'),
]