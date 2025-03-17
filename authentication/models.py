from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import BaseModel


class AuthUser(BaseModel, AbstractUser):
    class AuthUserSocialProviderEnum(models.TextChoices):
        EMAIL = "email", "이메일"
        GOOGLE = "google", "구글"

    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    social_id = models.CharField(max_length=255, blank=True)
    social_provider = models.CharField(
        max_length=50,
        choices=AuthUserSocialProviderEnum.choices,
        default=AuthUserSocialProviderEnum.EMAIL,
    )
    locale = models.CharField(max_length=10, blank=True)

    class Meta:
        db_table = "user"
