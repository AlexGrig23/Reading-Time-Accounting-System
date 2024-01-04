from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    year = models.IntegerField()
    short_description = models.TextField(max_length=128)
    full_description = models.TextField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.title


class ReadingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
