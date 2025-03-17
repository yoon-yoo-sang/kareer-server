from django.utils import timezone

from authentication.models import AuthUser
from users.models import UserCareerExperience, UserEducation, UserProfile
from users.serializers import (UserCareerExperienceSerializer,
                               UserEducationSerializer, UserProfileSerializer)


class UserWholeCareerServices:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_user_whole_career(self):
        user = AuthUser.objects.get(id=self.user_id)
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise UserProfile.DoesNotExist
        user_carrier_experiences = UserCareerExperience.objects.filter(
            user=user, deleted_at__isnull=True
        )
        user_educations = UserEducation.objects.filter(
            user=user, deleted_at__isnull=True
        )

        user_profile_serializer = UserProfileSerializer(user_profile)
        user_carrier_serializer = UserCareerExperienceSerializer(
            user_carrier_experiences, many=True
        )
        user_education_serializer = UserEducationSerializer(user_educations, many=True)

        return {
            "username": user.username,
            "email": user.email,
            "locale": user.locale,
            "social_provider": user.social_provider,
            "profile": user_profile_serializer.data,
            "career_experiences": user_carrier_serializer.data,
            "educations": user_education_serializer.data,
        }

    def update_user_whole_career(self, request_data):
        user = AuthUser.objects.get(id=self.user_id)
        user_profile = UserProfile.objects.get(user=user)
        user_carrier_experiences = UserCareerExperience.objects.filter(
            user=user, deleted_at__isnull=True
        )
        user_educations = UserEducation.objects.filter(
            user=user, deleted_at__isnull=True
        )

        user_profile_serializer = UserProfileSerializer(
            user_profile, data=request_data.get("profile")
        )
        user_profile_serializer.is_valid(raise_exception=True)
        user_profile_serializer.save()

        if user_carrier_experiences.exists():
            user_carrier_experiences.update(deleted_at=timezone.now())
        if user_educations.exists():
            user_educations.update(deleted_at=timezone.now())

        user_carrier_serializer = UserCareerExperienceSerializer(
            data=request_data.get("career_experiences"), many=True
        )
        user_carrier_serializer.is_valid(raise_exception=True)
        user_carrier_serializer.save(user=user)

        user_education_serializer = UserEducationSerializer(
            data=request_data.get("educations"), many=True
        )
        user_education_serializer.is_valid(raise_exception=True)
        user_education_serializer.save(user=user)

        return {
            "username": user.username,
            "email": user.email,
            "locale": user.locale,
            "social_provider": user.social_provider,
            "profile": user_profile_serializer.data,
            "career_experiences": user_carrier_serializer.data,
            "educations": user_education_serializer.data,
        }
