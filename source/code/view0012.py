from django.views.generic.detail import DetailView
from .models import Paste
from django.views.generic.edit import CreateView

class PasteCreate(CreateView):
    model = Paste
    fields = ['text','name']

class PasteDetail(DetailView):
    model = Paste
    template_name = "pastebin/paste_detail.html"