from django.utils import timezone
from rest_framework import serializers

from jobs.models import Job, JobApplication, JobBookmark, JobPostingRequest


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "company_name",
            "location",
            "requirements",
            "salary_range",
            "category",
            "industry",
            "posted_at",
            "expired_at",
            "is_hiring",
        ]
        read_only_fields = ["id", "posted_at"]


class AdminJobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "company_name",
            "location",
            "requirements",
            "salary_range",
            "category",
            "industry",
            "posted_at",
            "expired_at",
            "is_hiring",
            "created_by",
        ]
        read_only_fields = ["id", "posted_at", "created_by"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            "user",
            "job",
            "status",
            "cover_letter",
            "resume_uri",
            "applied_at",
        ]


class JobBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobBookmark
        fields = [
            "user",
            "job",
            "bookmarked_at",
        ]


class JobPostingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostingRequest
        fields = [
            "id",
            "title",
            "description",
            "company_name",
            "location",
            "requirements",
            "salary_range",
            "category",
            "industry",
            "status",
            "requested_by",
            "reviewed_by",
            "review_comment",
            "reviewed_at",
            "created_job",
        ]
        read_only_fields = [
            "id",
            "status",
            "requested_by",
            "reviewed_by",
            "review_comment",
            "reviewed_at",
            "created_job",
        ]
