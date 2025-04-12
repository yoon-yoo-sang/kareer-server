from django.contrib import admin
from django.utils import timezone

from jobs.models import Job, JobApplication, JobBookmark, JobPostingRequest


@admin.register(JobPostingRequest)
class JobPostingRequestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "company_name",
        "category",
        "industry",
        "status",
        "requested_by",
        "reviewed_by",
        "reviewed_at",
    ]
    list_filter = ["status", "category", "industry"]
    search_fields = ["title", "company_name", "description"]
    readonly_fields = [
        "requested_by",
        "reviewed_by",
        "reviewed_at",
        "created_job",
    ]
    actions = ["approve_requests", "reject_requests"]

    def approve_requests(self, request, queryset):
        for posting_request in queryset.filter(
            status=JobPostingRequest.StatusEnum.PENDING
        ):
            # Create a new job posting
            job = Job.objects.create(
                title=posting_request.title,
                description=posting_request.description,
                company_name=posting_request.company_name,
                location=posting_request.location,
                requirements=posting_request.requirements,
                salary_range=posting_request.salary_range,
                category=posting_request.category,
                industry=posting_request.industry,
                created_by=posting_request.requested_by,
            )

            # Update the request
            posting_request.status = JobPostingRequest.StatusEnum.APPROVED
            posting_request.reviewed_by = request.user
            posting_request.reviewed_at = timezone.now()
            posting_request.created_job = job
            posting_request.review_comment = "관리자에 의해 승인되었습니다."
            posting_request.save()

    approve_requests.short_description = "선택된 요청을 승인"

    def reject_requests(self, request, queryset):
        queryset.filter(status=JobPostingRequest.StatusEnum.PENDING).update(
            status=JobPostingRequest.StatusEnum.REJECTED,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
            review_comment="관리자에 의해 거절되었습니다.",
        )

    reject_requests.short_description = "선택된 요청을 거절"

    def has_add_permission(self, request):
        return False  # 관리자 페이지에서 직접 생성 방지


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "company_name",
        "category",
        "industry",
        "is_hiring",
        "posted_at",
        "expired_at",
        "created_by",
    ]
    list_filter = ["category", "industry", "is_hiring"]
    search_fields = ["title", "company_name", "description"]
    readonly_fields = ["posted_at", "created_by"]


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "job",
        "status",
        "applied_at",
    ]
    list_filter = ["status"]
    search_fields = ["user__email", "job__title"]
    readonly_fields = ["applied_at"]


@admin.register(JobBookmark)
class JobBookmarkAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "job",
        "bookmarked_at",
    ]
    search_fields = ["user__email", "job__title"]
    readonly_fields = ["bookmarked_at"]
