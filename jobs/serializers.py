from rest_framework import serializers

from jobs.models import Job, JobApplication, JobBookmark


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'description',
            'company_name',
            'location',
            'requirements',
            'salary_range',
            'category',
            'industry',
            'posted_at',
            'expired_at',
            'is_hiring',
        ]


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            'user',
            'job',
            'status',
            'cover_letter',
            'resume_uri',
            'applied_at',
        ]


class JobBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobBookmark
        fields = [
            'user',
            'job',
            'bookmarked_at',
        ]
