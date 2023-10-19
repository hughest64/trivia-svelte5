import datetime

from django.db import models
from django.utils import timezone


class ChangeLog(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=120)
    version = models.CharField(max_length=120, unique=True)
    notes = models.TextField()

    def __str__(self):
        return self.title

    def to_json(self):
        return {
            "id": self.id,
            "date": datetime.date.isoformat(self.created_at),
            "title": self.title,
            "version": self.version,
            "notes": self.notes,
        }
