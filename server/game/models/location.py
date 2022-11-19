from django.db import models
from django.forms.models import model_to_dict


class Location(models.Model):
    name = models.CharField(max_length=128)
    address = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    primary_host = models.ForeignKey(
        "user.User", blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    def to_json(self):
       return {
        "location_id": self.pk,
        "location_name": self.name
       }

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        