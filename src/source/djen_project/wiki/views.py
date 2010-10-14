# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext

from models import Article
from forms import ArticleForm, EditForm, ArticleEditForm

@login_required
def add_article(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        return redirect(article)
    return render_to_response('wiki/article_form.html', 
                              { 'form': form },
                              context_instance=RequestContext(request))


def edit_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article_form = ArticleForm(instance=article)
    edit_form = EditForm(request.POST or None)
    if request.method == "POST":
        article_form = ArticleEditForm(request.POST)
        if article_form.is_valid():
            article = article_form.save()
            edit_form = ArticleEditForm(request.POST, instance=article)
            if edit_form.is_valid():
                edit = edit_form.save()
                return redirect(article)
    return render_to_response('wiki/article_edit_form.html', 
                              { 
                                  'article_form': article_form,
                                  'edit_form': edit_form,
                              },
                              context_instance=RequestContext(request))

