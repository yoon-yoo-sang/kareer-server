from django.urls import include, path
from rest_framework.routers import DefaultRouter

from jobs.views import (JobApplicationViewSet, JobBookmarkViewSet,
                        JobPostingRequestViewSet, JobViewSet)

app_name = "jobs"

router = DefaultRouter()

router.register(r"jobs", JobViewSet, basename="job")
router.register(r"applications", JobApplicationViewSet, basename="job-application")
router.register(r"bookmarks", JobBookmarkViewSet, basename="job-bookmark")
router.register(
    r"posting-requests", JobPostingRequestViewSet, basename="job-posting-request"
)

urlpatterns = [
    path("", include(router.urls)),
]
