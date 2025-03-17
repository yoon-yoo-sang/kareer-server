from django.urls import path

from users.views import (MyProfileView, MySettingView, MyUserView,
                         MyWholeCareerView, MyBookmarkedJobsView, MyJobApplicationsView)

app_name = "users"

urlpatterns = [
    path("me", MyUserView.as_view(), name="me"),
    path("me/profile", MyProfileView.as_view(), name="me-profile"),
    path("me/setting", MySettingView.as_view(), name="me-setting"),
    path("me/whole-career", MyWholeCareerView.as_view(), name="me-whole-career"),
    path("me/bookmarked-jobs", MyBookmarkedJobsView.as_view(), name="me-bookmarked-jobs"),
    path("me/job-applications", MyJobApplicationsView.as_view(), name="me-job-applications"),
]
