# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from forms import PostForm

@login_required
def add_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(post)
    return render_to_response('blog/add_post.html', 
                              { 'form': form },
                              context_instance=RequestContext(request))

