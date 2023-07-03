from rest_framework import generics
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiExample,
)
from rest_framework.decorators import action
from django.db.models import Count, Sum


from common.serializer import (
    OperationError,
    OperationSuccess,
)
from common.pagination import CustomPagination
from task.models import Location
from task.api.serializers.task import (
    TaskSerializer,
    TaskListSerializer,
)
from rest_framework.filters import SearchFilter


@extend_schema_view(
    post=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="a)File Read Api(Use Postman to check the file read Api)",
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


@extend_schema_view(
    get=extend_schema(
        description="b)Project List API",
        summary="Refer to schemas at the bottom",
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success response when the project is listed successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="JSON Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Task Apis"],
    ),
)
class TaskListViewSet(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = TaskListSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = [
        "sector",
        "counterpart_ministry",
        "project_status",
        "agreement_date",
    ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "title": "Project List",
                "message": "Listed Successfully!",
                "data": serializer.data,
            }
        )


@extend_schema_view(
    get=extend_schema(
        description="c)Summary List API",
        summary="Refer to schemas at the bottom",
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success response when the summary is listed successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="JSON Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Task Apis"],
    ),
)
class TaskSummaryListViewSet(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = TaskListSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = [
        "sector",
        "counterpart_ministry",
        "project_status",
        "agreement_date",
    ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer_data = serializer.data
        else:
            serializer = self.get_serializer(queryset, many=True)
            serializer_data = serializer.data

        project_count = queryset.count()
        total_budget = queryset.aggregate(total_budget=Sum("commitments"))[
            "total_budget"
        ]
        sector_counts = queryset.values("sector").annotate(
            project_count=Count("sector"), budget=Sum("commitments")
        )
        summary_data = {
            "project_count": project_count,
            "total_budget": total_budget,
            "sector": [
                {
                    "id": count + 1,
                    "name": item["sector"],
                    "project_count": item["project_count"],
                    "budget": item["budget"],
                }
                for count, item in enumerate(sector_counts)
            ],
        }
        response_data = {
            "title": "Summary List",
            "message": "Listed Successfully!",
            "summary": summary_data,
        }
        if page is not None:
            response_data["pagination"] = self.get_paginated_response(
                serializer_data
            ).data
        return Response(response_data)


@extend_schema_view(
    get=extend_schema(
        description="d)Zone List API",
        summary="Refer to schemas at the bottom",
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success response when the project is listed successfully!",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="JSON Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Task Apis"],
    ),
)
class TaskOnlyListViewSet(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = TaskListSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ["province", "district"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer_data = serializer.data
        else:
            serializer = self.get_serializer(queryset, many=True)
            serializer_data = serializer.data

        group_by_data = queryset.values("muncipality", "district").annotate(
            count=Count("id"), budget=Sum("commitments")
        )
        response_data = {
            "title": "Zone List",
            "message": "Listed Successfully!",
            "data": [
                {
                    "id": count + 1,
                    "name": item["muncipality"],
                    "count": item["count"],
                    "budget": item["budget"],
                }
                for count, item in enumerate(group_by_data)
            ],
        }
        if page is not None:
            response_data["pagination"] = self.get_paginated_response(
                serializer_data
            ).data
        return Response(response_data)
