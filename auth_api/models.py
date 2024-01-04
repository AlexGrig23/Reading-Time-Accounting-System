from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserReadingStats(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="reading_stats"
    )
    statistic_time_7_days = models.DurationField(default=timedelta(days=0))
    statistic_time_30_days = models.DurationField(default=timedelta(days=0))

    def __str__(self):
        return f"Reading statistics for {self.user.username}"


@receiver(post_save, sender=User)
def create_user_reading_stats(sender, instance, created, **kwargs):
    if created:
        UserReadingStats.objects.create(user=instance)
