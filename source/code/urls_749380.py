from django.urls import re_path
from .views import PasteCreate

urlpatterns = [
	re_path(r'^$', PasteCreate.as_view(), name='create'),
]