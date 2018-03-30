from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import login

urlpatterns = [
    path(r'accounts/login/', login),
    path(r'admin/', admin.site.urls),
    path(r'pastebin/', include('pastebin.urls')),
    path(r'blog/', include('blog.urls')),
]
