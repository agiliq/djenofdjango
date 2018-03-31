from django.shortcuts import render
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

class PasteUpdate(UpdateView):
	model = Paste