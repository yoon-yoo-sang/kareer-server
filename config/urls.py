from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from authentication.views import PingView
from config.settings import DEBUG

schema_view = get_schema_view(
    openapi.Info(
        title="Kareer Server API",
        default_version="1",
        description="API docs for Kareer Server",
        terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(name="test", email="test@test.com"),
        # license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=[
        AllowAny,
    ],
)


urlpatterns = [
    # ping
    path("ping", PingView.as_view(), name="ping"),
    # Authentication
    path("auth/", include(("authentication.urls", "auth"), namespace="auth")),
    # Users
    path("users/", include(("users.urls", "users"), namespace="users")),
    # Jobs
    path("jobs/", include(("jobs.urls", "jobs"), namespace="jobs")),
    # Django admin
    path("admin/", admin.site.urls),
    # static files
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico")),
]

if DEBUG:
    urlpatterns += [
        path(
            "swagger<format>/",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
        path("silk/", include("silk.urls", namespace="silk")),
    ]
