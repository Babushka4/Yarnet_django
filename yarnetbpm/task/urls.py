from django.urls import path

from task.views import TaskInfo, TaskTable, AddNewTask

urlpatterns = [
    path('', TaskTable.as_view()),
    path('<int:id>', TaskTable.as_view()),
    path('new_task/', AddNewTask.as_view()),
    path('task_info/', TaskInfo.as_view())
]