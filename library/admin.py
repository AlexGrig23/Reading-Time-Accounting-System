from django.contrib import admin

from library.models import Book, ReadingSession

admin.site.register(Book)
admin.site.register(ReadingSession)
