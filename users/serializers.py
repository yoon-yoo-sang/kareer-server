from rest_framework import serializers

from authentication.models import AuthUser
from users.models import UserProfile, UserSetting, UserCareerExperience, UserEducation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = [
            'id',
            'username',
            'email',
            'locale',
            'social_provider',
        ]


class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        fields = [
            'is_email_notification_enabled',
            'is_push_notification_enabled',
            'language',
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'full_name',
            'nickname',
            'nationality',
            'occupation',
            'skills',
            'resume_uri',
        ]


class UserCareerExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCareerExperience
        fields = [
            'company_name',
            'job_title',
            'started_at',
            'ended_at',
            'description',
            'is_current',
        ]


class UserEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEducation
        fields = [
            'school_name',
            'major',
            'degree',
            'started_at',
            'ended_at',
            'description',
            'is_current',
        ]

class UserWholeCareerSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    career_experiences = UserCareerExperienceSerializer(many=True)
    educations = UserEducationSerializer(many=True)

    class Meta:
        model = AuthUser
        fields = [
            'id',
            'username',
            'email',
            'locale',
            'social_provider',
            'profile',
            'career_experiences',
            'educations',
        ]
