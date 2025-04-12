from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import IsStaffUser
from common.utils import get_object_or_404_response
from jobs.models import Job, JobApplication, JobBookmark, JobPostingRequest
from jobs.serializers import (AdminJobPostingSerializer,
                              JobApplicationSerializer, JobBookmarkSerializer,
                              JobPostingRequestSerializer, JobSerializer)
from jobs.services.job_search_services import JobSearchService


class JobViewSet(viewsets.GenericViewSet, RetrieveModelMixin, ListModelMixin):
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Job.objects.filter(deleted_at__isnull=True)
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            if self.action not in SAFE_METHODS:
                return AdminJobPostingSerializer
        return JobSerializer

    def get_permission_classes(self):
        if self.action not in SAFE_METHODS:
            return [IsStaffUser]
        return [IsAuthenticated]

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

class JobPostingRequestViewSet(viewsets.GenericViewSet, CreateModelMixin):
    queryset = JobPostingRequest.objects.all()
    serializer_class = JobPostingRequestSerializer

    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)


class JobBookmarkViewSet(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin):
    queryset = JobBookmark.objects.all()
    serializer_class = JobBookmarkSerializer

    def list(self, request: Request, *args, **kwargs):
        user = self.request.user
        bookmarks = user.bookmarks.filter(deleted_at__isnull=True)
        jobs = Job.objects.filter(bookmarks__in=bookmarks)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
        user = self.request.user
        job = Job.objects.get(id=request.data["job_id"])

        if JobBookmark.objects.filter(
            user=user, job=job, deleted_at__isnull=True
        ).exists():
            return Response(
                {"detail": "이미 북마크한 채용공고입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = JobBookmarkSerializer(data={"user": user.id, "job": job.id})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, job=job)
        return Response(status=status.HTTP_201_CREATED)

    @transaction.atomic
    def destroy(self, request: Request, *args, **kwargs):
        user = self.request.user
        job = Job.objects.get(id=request.data["job_id"])
        JobBookmark.objects.filter(user=user, job=job).update(deleted_at=timezone.now())
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobApplicationViewSet(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    def list(self, request: Request, *args, **kwargs):
        user = self.request.user
        applications = user.applications.filter(deleted_at__isnull=True)
        serializer = JobApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
        user = self.request.user
        job = Job.objects.get(id=request.data["job_id"])

        if user.applications.filter(job=job, deleted_at__isnull=True).exists():
            return Response(
                {"detail": "이미 지원한 채용공고입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = JobApplicationSerializer(data={"user": user.id, "job": job.id})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, job=job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def destroy(self, request: Request, *args, **kwargs):
        user = self.request.user

        pk = request.parser_context["kwargs"]["pk"]
        job = Job.objects.get(id=pk)
        application = get_object_or_404_response(JobApplication, user=user, job=job)
        application.deleted_at = timezone.now()
        application.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
