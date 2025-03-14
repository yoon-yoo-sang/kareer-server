from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    deleted_at = models.DateTimeField(db_index=True, null=True)

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    class Meta:
        abstract = True
