from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import UserProfile, UserSetting
from users.serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserSettingSerializer,
    UserWholeCareerSerializer
)
from users.services.user_whole_career_services import UserWholeCareerServices


class MyUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request: Request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'UserProfile이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request: Request):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        if not created:
            return Response({'detail': 'UserProfile은 이미 존재함'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request: Request):
        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'UserProfile이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MySettingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        try:
            setting = UserSetting.objects.get(user=self.request.user)
        except UserSetting.DoesNotExist:
            return Response({'detail': 'UserSetting이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSettingSerializer(setting)
        return Response(serializer.data)

    def post(self, request: Request):
        setting, created = UserSetting.objects.get_or_create(user=self.request.user)
        if not created:
            return Response({'detail': 'UserSetting은 이미 존재함'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSettingSerializer(setting, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request: Request):
        try:
            setting = UserSetting.objects.get(user=self.request.user)
        except UserSetting.DoesNotExist:
            return Response({'detail': 'UserSetting이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSettingSerializer(setting, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MyWholeCareerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        services = UserWholeCareerServices(self.request.user.id)
        try:
            data = services.get_user_whole_career()
        except UserProfile.DoesNotExist:
            return Response({'detail': 'UserProfile이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserWholeCareerSerializer(data)
        return Response(serializer.data)

    def patch(self, request: Request):
        services = UserWholeCareerServices(self.request.user.id)
        try:
            updated_data = services.update_user_whole_career(request.data)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'UserProfile이 존재하지 않음'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserWholeCareerSerializer(updated_data)
        return Response(serializer.data)
