from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.errors import (USER_PROFILE_ALREADY_EXISTS,
                           USER_SETTING_ALREADY_EXISTS)
from common.utils import get_object_or_404_response
from jobs.models import Job, JobApplication, JobBookmark
from jobs.serializers import (JobApplicationSerializer, JobBookmarkSerializer,
                              JobSerializer)
from users.models import UserProfile, UserSetting
from users.serializers import (UserProfileSerializer, UserSerializer,
                               UserSettingSerializer,
                               UserWholeCareerSerializer)
from users.services.user_whole_career_services import UserWholeCareerServices


class MyUserView(APIView):
    def get(self, request: Request):
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)

    @transaction.atomic
    def patch(self, request: Request):
        serializer = UserSerializer(self.request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MyProfileView(APIView):
    def get(self, request: Request):
        profile = get_object_or_404_response(UserProfile, user=self.request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request: Request):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        if not created:
            return Response(
                {"detail": USER_PROFILE_ALREADY_EXISTS},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UserProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def patch(self, request: Request):
        profile = get_object_or_404_response(UserProfile, user=self.request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MySettingView(APIView):
    def get(self, request: Request):
        setting = get_object_or_404_response(UserSetting, user=self.request.user)
        serializer = UserSettingSerializer(setting)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request: Request):
        setting, created = UserSetting.objects.get_or_create(user=self.request.user)
        if not created:
            return Response(
                {"detail": USER_SETTING_ALREADY_EXISTS},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UserSettingSerializer(setting, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def patch(self, request: Request):
        setting = get_object_or_404_response(UserSetting, user=self.request.user)
        serializer = UserSettingSerializer(setting, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MyWholeCareerView(APIView):
    def get(self, request: Request):
        services = UserWholeCareerServices(self.request.user.id)
        data = services.get_user_whole_career()
        serializer = UserWholeCareerSerializer(data)
        return Response(serializer.data)

    @transaction.atomic
    def patch(self, request: Request):
        services = UserWholeCareerServices(self.request.user.id)
        updated_data = services.update_user_whole_career(request.data)
        serializer = UserWholeCareerSerializer(updated_data)
        return Response(serializer.data)


class MyBookmarkedJobsView(APIView):
    def get(self, request: Request):
        user = self.request.user
        bookmarks = user.bookmarks.filter(deleted_at__isnull=True)
        jobs = Job.objects.filter(bookmarks__in=bookmarks)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request: Request):
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
    def delete(self, request: Request):
        user = self.request.user
        job = Job.objects.get(id=request.data["job_id"])
        JobBookmark.objects.filter(user=user, job=job).update(deleted_at=timezone.now())
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyJobApplicationsView(APIView):
    def get(self, request: Request):
        user = self.request.user
        applications = user.applications.filter(deleted_at__isnull=True)
        serializer = JobApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request: Request):
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
    @action(detail=True, methods=["delete"])
    def delete(self, request: Request):
        user = self.request.user

        pk = request.parser_context["kwargs"]["pk"]
        job = Job.objects.get(id=pk)
        application = get_object_or_404_response(JobApplication, user=user, job=job)
        application.deleted_at = timezone.now()
        application.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
