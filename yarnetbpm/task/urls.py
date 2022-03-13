from django.urls import path, re_path

from task.views import (
    TaskInfo,
    TaskTable,
    AddNewTask,
    ReassignPerformer,
    
    get_form,
    get_sidebar_body,
    get_view_task_body,
    get_view_task_history
)

urlpatterns = [
    re_path('.*', TaskTable.as_view()),
    path('<int:id>', TaskTable.as_view()),
    path('new_task/', AddNewTask.as_view()),
    path('task_info/', TaskInfo.as_view()),
    path('reassign/', ReassignPerformer.as_view()),

    path('get-form/', get_form),
    path('get-sidebar-body/', get_sidebar_body),
    path('get-view-task-body/', get_view_task_body),
    path('get-view-task-history/', get_view_task_history),
]