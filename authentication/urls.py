from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import SignInView, SignUpView

app_name = "auth"

urlpatterns = [
    path("sign-up", SignUpView.as_view(), name="sign-up"),
    path("sign-in", SignInView.as_view(), name="sign-in"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
