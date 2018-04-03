"""djen_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import path, include
    2. Add a URL to urlpatterns:  path(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import login

urlpatterns = [
    path('accounts/login/', login),
    path('admin/', admin.site.urls),
    path('pastebin/', include('pastebin.urls')),
    path('blog/', include('blog.urls')),
    path('wiki/', include('wiki.urls')),
]
