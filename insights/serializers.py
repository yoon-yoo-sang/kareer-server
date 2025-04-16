from rest_framework import serializers

from insights.models import CultureInfo, IndustryInfo, VisaInfo


class VisaInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for VisaInfo model.
    """

    class Meta:
        model = VisaInfo
        fields = [
            "visa_type",
            "requirements",
            "process",
            "duration",
        ]


class CultureInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for CultureInfo model.
    """

    class Meta:
        model = CultureInfo
        fields = [
            "culture_type",
            "title",
            "content",
            "tags",
            "source_urls",
        ]


class IndustryInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for IndustryInfo model.
    """

    class Meta:
        model = IndustryInfo
        fields = [
            "industry_type",
            "description",
            "trends",
            "opportunities",
        ]
