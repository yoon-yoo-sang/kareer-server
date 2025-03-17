from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import AuthUser
from authentication.strategies import (EmailAuthenticationStrategy,
                                       SocialAuthenticationStrategy)


class AuthenticationService:
    STRATEGIES = {
        "social": SocialAuthenticationStrategy(),
        "email": EmailAuthenticationStrategy(),
    }

    @classmethod
    def get_strategy(cls, **credentials):
        if "social_id" in credentials:
            return cls.STRATEGIES["social"]
        elif "email" in credentials:
            return cls.STRATEGIES["email"]
        else:
            raise ValueError("사용자 인증에 필요한 정보가 부족합니다")

    @staticmethod
    def generate_token(user: AuthUser):
        refresh = RefreshToken.for_user(user)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

    def authenticate(self, **credentials):
        strategy = self.get_strategy(**credentials)
        user = strategy.authenticate(**credentials)
        return self.generate_token(user)

    def signup(self, **credentials):
        strategy = self.get_strategy(**credentials)
        user = strategy.signup(**credentials)
        return self.generate_token(user)
