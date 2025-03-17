from authentication.interfaces import AuthenticationStrategyInterface
from authentication.models import AuthUser
from common.errors import (AUTH_USER_ALREADY_EXISTS, EMAIL_ALREADY_EXISTS,
                           EMAIL_OR_PASSWORD_INCORRECT)
from common.utils import get_object_or_404_response


class SocialAuthenticationStrategy(AuthenticationStrategyInterface):
    def authenticate(self, social_id: str):
        return get_object_or_404_response(AuthUser, social_id=social_id)

    def signup(
        self, social_id: str, social_provider: str, email: str, locale: str = ""
    ):
        if AuthUser.objects.filter(social_id=social_id).exists():
            raise ValueError(AUTH_USER_ALREADY_EXISTS)

        if AuthUser.objects.filter(email=email).exists():
            raise ValueError(EMAIL_ALREADY_EXISTS)

        user = AuthUser.objects.create_user(
            username=f"{social_provider}_{social_id}",
            social_id=social_id,
            social_provider=social_provider,
            email=email,
            locale=locale,
        )

        return user


class EmailAuthenticationStrategy(AuthenticationStrategyInterface):
    def authenticate(self, email: str, password: str):
        user = get_object_or_404_response(AuthUser, email=email)
        if not user or not user.check_password(password):
            raise ValueError(EMAIL_OR_PASSWORD_INCORRECT)
        return user

    def signup(self, email: str, password: str, locale: str = ""):
        if AuthUser.objects.filter(email=email).exists():
            raise ValueError(EMAIL_ALREADY_EXISTS)

        user = AuthUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            social_provider=AuthUser.AuthUserSocialProviderEnum.EMAIL,
            locale=locale,
        )

        return user
