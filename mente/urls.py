from django.urls import path, include

from . import views

app_name = 'mente'

urlpatterns = [
    path('shou_registration', views.shou_registration, name = 'shou_registration'),
    path('registration/<int:shou_id>', views.registration, name = 'registration'),
    path('pre_registration', views.pre_registration, name = 'pre_registration'),
    path('pre_edit', views.pre_edit, name = 'pre_edit'),
    path('edit/<int:pk>/', views.Edit.as_view(), name='edit'),
    path('pre_delete', views.pre_delete, name = 'pre_delete'),
    path('delete/<int:pk>/', views.Delete.as_view(), name = 'delete'),
]
