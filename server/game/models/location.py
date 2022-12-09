from django.db import models

class Location(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
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
        