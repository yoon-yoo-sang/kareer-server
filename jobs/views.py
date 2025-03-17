from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from jobs.models import Job
from jobs.serializers import JobSerializer
from jobs.services.job_search_services import JobSearchService


class JobModelViewSet(viewsets.GenericViewSet, RetrieveModelMixin, ListModelMixin):
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Job.objects.filter(deleted_at__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = JobSerializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        service = JobSearchService(self.get_queryset())
        search = request.query_params.get("search")
        category = request.query_params.get("category")
        industry = request.query_params.get("industry")
        order_by = request.query_params.get("order_by")

        queryset = service.filter_jobs(search, category, industry, order_by)
        queryset = self.paginate_queryset(queryset)

        serializer = JobSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)
