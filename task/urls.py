from django.urls import path
from task.api.viewsets.task import (
    TaskCreateView,
    TaskListViewSet,
    TaskSummaryListViewSet,
    TaskOnlyListViewSet,
)

urlpatterns = [
    path("file-read/", TaskCreateView.as_view()),
    path("project-list/", TaskListViewSet.as_view()),
    path("summary-list/", TaskSummaryListViewSet.as_view()),
    path("zone-list/", TaskOnlyListViewSet.as_view()),
]
