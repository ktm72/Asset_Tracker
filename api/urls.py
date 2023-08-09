from django.urls import path
from . import views


urlpatterns = [
    path('test', views.test, name='test'),
    path('company', views.company, name='company'),
    path('company/<int:company_id>', views.company_detail, name='company_detail'),
    path('employee', views.employee, name='employee'),
    path('employee/<int:employee_id>',
         views.employee_details, name='employee_details'),
    path('company/<int:company_id>/employees',
         views.company_employees, name='company_employees'),
]
