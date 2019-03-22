from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('admin/', admin.site.urls),
    path('item/', include('item.urls')),
    path('mente/', include('mente.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
