from django.urls import path
from . import views


urlpatterns = [
    path('test', views.test, name='test'),
    path('company', views.company, name='company'),
    path('company/<int:company_id>', views.company_details, name='company_detail'),

    path('employee', views.employee, name='employee'),
    path('employee/<int:employee_id>',
         views.employee_details, name='employee_details'),
    path('company/<int:company_id>/employees',
         views.company_employees, name='company_employees'),

    path('gear', views.gear, name='gear'),
    path('gear/<int:gear_id>', views.gear_details, name='gear_detail'),
    path('company/<int:company_id>/gears',
         views.company_gears, name='company_gears'),

    path('gear-log', views.gear_log, name='gear_log'),
    path('gear-log/<int:log_id>', views.gear_log_details, name='gear_log_details'),
    path('company/<int:company_id>/logs/',
         views.company_logs, name='company_logs'),
    path('employee/<int:employee_id>/logs',
         views.employee_logs, name='employee_logs'),
]
