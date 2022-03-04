from django.urls import path

from user.views import UserTable

urlpatterns = [
    path('', UserTable.as_view())   
]