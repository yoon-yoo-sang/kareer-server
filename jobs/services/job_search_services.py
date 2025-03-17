from django.db.models import Q, Count
from django.utils import timezone


class JobSearchService:
    def __init__(self, queryset):
        self.queryset = queryset

    def filter_jobs(self, search: str = '', category: str = '', industry: str = '', order_by: str = ''):
        self.queryset = self.queryset.filter(deleted_at__isnull=True)
        self.queryset = self.queryset.filter(expired_at__gte=timezone.now())

        if search:
            self.queryset = self.queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

        if category:
            self.queryset = self.queryset.filter(category=category)

        if industry:
            self.queryset = self.queryset.filter(industry=industry)

        if order_by:
            if order_by == 'recently':
                self.queryset = self.queryset.order_by('-posted_at')
            if order_by == 'recommended':
                self.get_recommended_count_of_jobs()
                self.queryset = self.queryset.order_by('-recommended_count')

        return self.queryset

    def get_recommended_count_of_jobs(self):
        # TODO: 추천 로직 고도화
        self.queryset = self.queryset.prefetch_related('bookmarks')
        self.queryset = self.queryset.annotate(recommended_count=Count('bookmarks'))
