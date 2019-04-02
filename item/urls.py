from django.urls import path, include

from . import views

app_name = 'item'

urlpatterns = [
    path('top_page/', views.top_page, name = 'top_page'),
    path('test_check/', views.test_check, name = 'test_check'),
    path('prob_list/<int:shou_id>', views.prob_list, name = 'prob_list'),
    path('answer_page/<int:shou_id>/<int:prob_num>', views.answer_page, name = 'answer_page'),
]
