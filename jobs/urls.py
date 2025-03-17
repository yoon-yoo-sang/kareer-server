from rest_framework.routers import DefaultRouter

from jobs.views import JobModelViewSet

app_name = "jobs"

router = DefaultRouter()

router.register("jobs", JobModelViewSet, basename="jobs")

urlpatterns = router.urls
