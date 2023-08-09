from django.urls import path
from . import views


urlpatterns = [
    path('test/', views.test, name='test'),
    path('company/', views.company, name='company'),
    path('company/<int:company_id>', views.company_detail, name='company_detail'),
]
