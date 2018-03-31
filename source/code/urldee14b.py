from django.urls import re_path
from .views import PasteList, PasteDetail, PasteDelete, PasteUpdate, PasteCreate

urlpatterns = [
    re_path(r'', PasteCreate.as_view(), name='create'),
    re_path(r'^pastes/', PasteList.as_view(), name='pastebin_paste_list'),
    re_path(r'^paste/(?P<pk>\d+)$', PasteDetail.as_view(), name='pastebin_paste_detail'),
    re_path(r'^paste/delete/(?P<object_id>\d+)$', PasteUpdate.as_view()),
    re_path(r'^paste/edit/(?P<object_id>\d+)$', PasteDelete.as_view()),
]
