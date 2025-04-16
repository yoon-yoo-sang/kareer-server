from django.db import models

from common.models import BaseModel


class SearchKeyword(BaseModel):
    keyword = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    last_searched_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "search_keywords"
        indexes = [
            models.Index(fields=["is_active"], name="search_keywords_is_active_idx"),
        ]


class Insight(BaseModel):
    class CategoryEnum(models.TextChoices):
        VISA = "visa", "비자 정보"
        CULTURE = "culture", "문화 정보"
        INDUSTRY = "industry", "산업 정보"

    search_word = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CategoryEnum.choices)
    content = models.TextField()
    source_url = models.CharField(max_length=512, unique=True)

    class Meta:
        db_table = "insights"
        indexes = [
            models.Index(fields=["category"], name="insights_category_idx"),
            models.Index(fields=["search_word"], name="insights_search_word_idx"),
            models.Index(fields=["source_url"], name="insights_source_url_idx"),
        ]


class VisaInfo(BaseModel):
    visa_type = models.CharField(max_length=50, unique=True)
    requirements = models.JSONField()
    process = models.JSONField()
    duration = models.CharField(max_length=255)

    class Meta:
        db_table = "visa_info"
        indexes = [
            models.Index(fields=["visa_type"], name="visa_type_idx"),
        ]


class CultureInfo(BaseModel):
    class CultureTypeEnum(models.TextChoices):
        BUSINESS = "business", "비즈니스 문화"
        DAILY = "daily", "일상생활"
        SOCIAL = "social", "사회적 관습"
        FOOD = "food", "음식 문화"
        HOUSING = "housing", "주거 문화"
        TRANSPORTATION = "transportation", "교통"
        ENTERTAINMENT = "entertainment", "여가 생활"

    culture_type = models.CharField(
        max_length=50,
        choices=CultureTypeEnum.choices,
        unique=True,
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.JSONField()
    source_urls = models.JSONField(default=list)

    class Meta:
        db_table = "culture_info"
        indexes = [
            models.Index(fields=["culture_type"], name="culture_type_idx"),
        ]


class IndustryInfo(BaseModel):
    industry_type = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    trends = models.JSONField()
    opportunities = models.JSONField()

    class Meta:
        db_table = "industry_info"
        indexes = [
            models.Index(fields=["industry_type"], name="industry_type_idx"),
        ]
