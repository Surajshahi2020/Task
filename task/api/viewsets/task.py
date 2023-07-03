from rest_framework import generics
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiExample,
)

from common.serializer import (
    OperationError,
    OperationSuccess,
)
from common.pagination import CustomPagination
from task.models import Location
from task.api.serializers.task import TaskSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="File Read Api",
        request=TaskSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when file is read successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid file is sent!",
            ),
        },
        tags=["Task Apis"],
    ),
)
class TaskCreateView(generics.CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "File Read",
                "message": "File read successfully",
            }
        )
