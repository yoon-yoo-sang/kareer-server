from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from authentication.views import PingView

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
