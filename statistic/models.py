from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models

from library.models import Book


class ReadingStatistics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    total_reading_time = models.DurationField(default=timedelta())
