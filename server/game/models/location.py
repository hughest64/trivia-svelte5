from django.db import models


class Location(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    address = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    use_sound = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "location_id": self.pk,
            "location_name": self.name,
            "use_sound": self.use_sound,
        }

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
