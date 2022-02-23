from django.urls import path

from task.views import TaskTable

urlpatterns = [
    path('', TaskTable.as_view())   
]