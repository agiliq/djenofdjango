from django import forms

from models import Article

class ArticleForm(forms.ModelForm):
    summary = forms.CharField(max_length=100)

    class Meta:
        model = Article
        exclude = ['author', 'slug']

