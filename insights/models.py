from django.db import models

from common.models import BaseModel


class SearchKeyword(BaseModel):
    keyword = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    last_searched_at = models.DateTimeField(null=True)
    
    class Meta:
        db_table = "search_keywords"
        indexes = [
            models.Index(fields=['is_active'], name='search_keywords_is_active_idx'),
        ]


class Insight(BaseModel):
    class CategoryEnum(models.TextChoices):
        VISA = "visa", "비자 정보"
        CULTURE = "culture", "문화 정보"
        INDUSTRY = "industry", "산업 정보"
        
    search_word = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CategoryEnum.choices)
    content = models.TextField()
    source_url = models.TextField()
    
    class Meta:
        db_table = "insights"
        indexes = [
            models.Index(fields=['category'], name='insights_category_idx'),
            models.Index(fields=['search_word'], name='insights_search_word_idx'),
        ]
