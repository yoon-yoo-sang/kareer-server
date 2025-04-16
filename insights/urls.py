from django.urls import path

from insights.views import (CultureInfoViewSet, IndustryInfoViewSet,
                            VisaInfoViewSet)

app_name = "insights"

urlpatterns = [
    path("visa-info", VisaInfoViewSet.as_view(), name="visa-info"),
    path(
        "culture-info",
        CultureInfoViewSet.as_view(),
        name="culture-info",
    ),
    path(
        "industry-info",
        IndustryInfoViewSet.as_view(),
        name="industry-info",
    ),
]
