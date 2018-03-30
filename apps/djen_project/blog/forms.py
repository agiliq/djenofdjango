from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'slug']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']
