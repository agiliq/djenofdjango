from django import forms

from models import Article, Edit
from django.forms.models import inlineformset_factory

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author', 'slug']

class EditForm(forms.ModelForm):
    class Meta:
        model = Edit
        fields = ['summary']

ArticleEditForm = inlineformset_factory(Article, Edit, can_delete=False)

