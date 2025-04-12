from django.db import models

from common.models import BaseModel


class Job(BaseModel):
    class CategoryEnum(models.TextChoices):
        FULL_TIME = "full_time", "정규직"
        PART_TIME = "part_time", "파트타임"
        CONTRACT = "contract", "계약직"
        INTERNSHIP = "internship", "인턴십"
        TEMPORARY = "temporary", "일용직"
        REMOTE = "remote", "재택근무"
        FREELANCE = "freelance", "프리랜서"
        OTHER = "other", "기타"

    class IndustryEnum(models.TextChoices):
        INTERNET = "internet", "인터넷"
        FINTECH = "fintech", "핀테크"
        EDUCATION = "education", "교육"
        HEALTHCARE = "healthcare", "의료"
        E_COMMERCE = "e_commerce", "전자 상거래"
        REAL_ESTATE = "real_estate", "부동산"
        LOGISTICS = "logistics", "물류"
        MARKETPLACE = "marketplace", "마켓플레이스"
        SOCIAL_NETWORK = "social_network", "소셜 네트워크"
        OTHER = "other", "기타"

    title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    requirements = models.JSONField(default=list)
    # 예시: ["3년 이상의 Django 경험", "영어 의사소통 가능자"]
    salary_range = models.JSONField(default=dict, blank=True)
    # 예시: {"min": 40000, "max": 70000, "currency": "USD", "period": "yearly"}
    category = models.CharField(
        max_length=50, choices=CategoryEnum.choices, default=CategoryEnum.OTHER
    )
    industry = models.CharField(
        max_length=50, choices=IndustryEnum.choices, default=IndustryEnum.OTHER
    )
    posted_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True)
    is_hiring = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "authentication.AuthUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_jobs",
    )

    class Meta:
        db_table = "job"
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["industry"]),
            models.Index(fields=["posted_at"]),
            models.Index(fields=["expired_at"]),
            models.Index(fields=["is_hiring"]),
            models.Index(fields=["created_by"]),
        ]


class JobApplication(BaseModel):
    class StatusEnum(models.TextChoices):
        PENDING = "pending", "대기중"
        APPROVED = "approved", "승인됨"
        REJECTED = "rejected", "거부됨"

    user = models.ForeignKey(
        "authentication.AuthUser", on_delete=models.CASCADE, related_name="applications"
    )
    job = models.ForeignKey(
        "jobs.Job", on_delete=models.CASCADE, related_name="applications"
    )
    status = models.CharField(
        max_length=50, choices=StatusEnum.choices, default=StatusEnum.PENDING
    )
    cover_letter = models.TextField(blank=True)
    resume_uri = models.URLField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "job_application"
        indexes = [
            models.Index(fields=["applied_at"]),
        ]


class JobBookmark(BaseModel):
    user = models.ForeignKey(
        "authentication.AuthUser", on_delete=models.CASCADE, related_name="bookmarks"
    )
    job = models.ForeignKey(
        "jobs.Job", on_delete=models.CASCADE, related_name="bookmarks"
    )
    bookmarked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "job_bookmark"
        unique_together = ("user", "job")
        indexes = [
            models.Index(fields=["user", "bookmarked_at"]),
        ]


class JobPostingRequest(BaseModel):
    class StatusEnum(models.TextChoices):
        PENDING = "pending", "대기중"
        APPROVED = "approved", "승인됨"
        REJECTED = "rejected", "거절됨"

    title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    requirements = models.JSONField(default=list)
    salary_range = models.JSONField(default=dict, blank=True)
    category = models.CharField(
        max_length=50, choices=Job.CategoryEnum.choices, default=Job.CategoryEnum.OTHER
    )
    industry = models.CharField(
        max_length=50, choices=Job.IndustryEnum.choices, default=Job.IndustryEnum.OTHER
    )
    status = models.CharField(
        max_length=50, choices=StatusEnum.choices, default=StatusEnum.PENDING
    )
    requested_by = models.ForeignKey(
        "authentication.AuthUser",
        on_delete=models.CASCADE,
        related_name="job_posting_requests",
    )
    reviewed_by = models.ForeignKey(
        "authentication.AuthUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="reviewed_job_posting_requests",
    )
    review_comment = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True)
    created_job = models.OneToOneField(
        "jobs.Job", on_delete=models.SET_NULL, null=True, related_name="posting_request"
    )

    class Meta:
        db_table = "job_posting_request"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["requested_by"]),
            models.Index(fields=["reviewed_by"]),
        ]
