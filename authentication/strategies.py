from authentication.interfaces import AuthenticationStrategyInterface
from authentication.models import AuthUser


class SocialAuthenticationStrategy(AuthenticationStrategyInterface):
    def authenticate(self, social_id: str):
        try:
            user = AuthUser.objects.get(social_id=social_id)
            return user
        except AuthUser.DoesNotExist:
            raise ValueError('사용자가 존재하지 않습니다')

    def signup(self, social_id: str, social_provider: str, email: str, locale: str = ''):
        if AuthUser.objects.filter(social_id=social_id).exists():
            raise ValueError('이미 가입된 사용자입니다')

        if AuthUser.objects.filter(email=email).exists():
            raise ValueError('이미 가입된 이메일입니다')

        user = AuthUser.objects.create_user(
            username=f'{social_provider}_{social_id}',
            social_id=social_id,
            social_provider=social_provider,
            email=email,
            locale=locale,
        )

        return user


class EmailAuthenticationStrategy(AuthenticationStrategyInterface):
    def authenticate(self, email: str, password: str):
        try:
            user = AuthUser.objects.get(email=email)
            if not user or not user.check_password(password):
                raise ValueError('이메일 또는 비밀번호가 올바르지 않습니다')
            return user
        except AuthUser.DoesNotExist:
            raise ValueError('사용자가 존재하지 않습니다')

    def signup(self, email: str, password: str, locale: str = ''):
        if AuthUser.objects.filter(email=email).exists():
            raise ValueError('이미 가입된 이메일입니다')

        user = AuthUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            social_provider=AuthUser.AuthUserSocialProviderEnum.EMAIL,
            locale=locale,
        )

        return user
