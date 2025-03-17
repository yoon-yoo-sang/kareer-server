from django.conf import settings
from django.db import models

from common.models import BaseModel


class UserSetting(BaseModel):
    user = models.OneToOneField(
        "authentication.AuthUser",
        on_delete=models.CASCADE,
        related_name="setting",
    )
    is_email_notification_enabled = models.BooleanField(default=True)
    is_push_notification_enabled = models.BooleanField(default=True)
    language = models.CharField(max_length=10, choices=settings.LANGUAGES, default="ko")

    class Meta:
        db_table = "user_setting"


class UserProfile(BaseModel):
    class UserProfileOccupationEnum(models.TextChoices):
        DEVELOPER = "developer", "개발"
        BUSINESS = "business", "경영/비즈니스"
        DESIGNER = "designer", "디자인"
        MARKETER = "marketer", "마케팅"
        HR = "hr", "인사/채용"
        FINANCE = "finance", "재무/회계"
        LEGAL = "legal", "법률"
        EDUCATION = "education", "교육"
        MEDICAL = "medical", "의료"
        OTHER = "other", "기타"

    user = models.OneToOneField(
        "authentication.AuthUser",
        on_delete=models.CASCADE,
        related_name="profile",
    )
    full_name = models.CharField(max_length=255, blank=True)
    nickname = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    occupation = models.CharField(
        max_length=50,
        choices=UserProfileOccupationEnum.choices,
        default=UserProfileOccupationEnum.OTHER,
    )
    skills = models.JSONField(default=list)
    resume_uri = models.URLField(blank=True)

    class Meta:
        db_table = "user_profile"


class UserCareerExperience(BaseModel):
    user = models.ForeignKey(
        "authentication.AuthUser",
        on_delete=models.CASCADE,
        related_name="career_experiences",
    )
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    started_at = models.DateField()
    ended_at = models.DateField(null=True)
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        db_table = "user_career_experience"


class UserEducation(BaseModel):
    class DegreeEnum(models.TextChoices):
        HIGH = "high", "고졸"
        ASSOCIATE = "associate", "전문학사"
        BACHELOR = "bachelor", "학사"
        MASTER = "master", "석사"
        DOCTORATE = "doctorate", "박사"
        OTHER = "other", "기타"

    user = models.ForeignKey(
        "authentication.AuthUser",
        on_delete=models.CASCADE,
        related_name="educations",
    )
    school_name = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    degree = models.CharField(
        max_length=50,
        choices=DegreeEnum.choices,
        default=DegreeEnum.BACHELOR,
    )
    started_at = models.DateField()
    ended_at = models.DateField(null=True)
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        db_table = "user_education"
