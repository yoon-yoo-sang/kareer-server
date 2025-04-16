# Create your views here.
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin

from insights.models import CultureInfo, IndustryInfo, VisaInfo
from insights.serializers import (CultureInfoSerializer,
                                  IndustryInfoSerializer, VisaInfoSerializer)


class VisaInfoViewSet(viewsets.GenericViewSet, ListModelMixin):
    """
    A viewset for viewing visa information instances.
    """

    queryset = VisaInfo.objects.all()
    serializer_class = VisaInfoSerializer


class CultureInfoViewSet(viewsets.GenericViewSet, ListModelMixin):
    """
    A viewset for viewing culture information instances.
    """

    queryset = CultureInfo.objects.all()
    serializer_class = CultureInfoSerializer


class IndustryInfoViewSet(viewsets.GenericViewSet, ListModelMixin):
    """
    A viewset for viewing industry information instances.
    """

    queryset = IndustryInfo.objects.all()
    serializer_class = IndustryInfoSerializer
