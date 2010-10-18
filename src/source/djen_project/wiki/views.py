# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext

from models import Article
from forms import ArticleForm

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
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        article = form.save()
        return redirect(article)
    return render_to_response('wiki/article_form.html', 
                              { 
                                  'form': form,
                                  'article': article,
                              },
                              context_instance=RequestContext(request))

