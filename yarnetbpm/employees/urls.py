from django.urls import path

from employees.views import EmployeeTable

urlpatterns = [
    path('', EmployeeTable.as_view())   
]