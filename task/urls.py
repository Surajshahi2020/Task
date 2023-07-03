from django.urls import path
from task.api.viewsets.task import TaskCreateView

urlpatterns = [
    path("file-read/", TaskCreateView.as_view()),
]
