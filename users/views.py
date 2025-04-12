from django.db import transaction
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.errors import (USER_PROFILE_ALREADY_EXISTS,
                           USER_SETTING_ALREADY_EXISTS)
from common.utils import get_object_or_404_response
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
