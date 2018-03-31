from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Paste

# Create your views here

class PasteCreate(CreateView):
	model = Paste
	fields = ['text','name']

class PasteList(ListView):
	template_name = "pastebin/paste_list.html"
	def get_queryset(self):
		return Paste.objects.all()


class PasteDetail(DetailView):
	model = Paste
	template_name = "pastebin/paste_detail.html"

class PasteDelete(DeleteView):
	model = Paste
	success_url = reverse_lazy('pastebin_paste_list')

class PasteUpdate(UpdateView):
	model = Paste
	fields = ['text', 'name']