# Description: This file contains the tasks for updating the statistics of the users' reading time.

from datetime import timedelta

from celery import shared_task
from django.contrib.auth.models import User
from django.db.models import Case, ExpressionWrapper, F, Sum, When, fields
from django.utils import timezone

from auth_api.models import UserReadingStats
from library.models import ReadingSession


class UserReadingStatsUpdater:
    @staticmethod
    def update_reading_stats_for_user(user, date_from):
        """
        Calculates the total reading time for a given user (user),
        the duration of only a session that is partially or completely carried out in a given time interval.
        :param user: The user for whom statistics should be calculated.
        :param date_from: Start of the time interval for calculating statistics.
        :return: Total reading time during the specified interval.

        """
        total_reading_time = ReadingSession.objects.filter(
            user=user, end_time__gte=date_from, end_time__isnull=False
        ).annotate(
            adjusted_start_time=Case(
                When(start_time__gte=date_from, then=F("start_time")),
                default=date_from,
                output_field=fields.DateTimeField(),
            ),
            adjusted_end_time=F("end_time"),
        ).aggregate(
            total_time=Sum(
                ExpressionWrapper(
                    F("adjusted_end_time") - F("adjusted_start_time"),
                    output_field=fields.DurationField(),
                )
            )
        )[
            "total_time"
        ] or timedelta(
            0
        )

        return total_reading_time

    @classmethod
    def update_user_reading_stats(cls, days):
        """
        Updates reading statistics for all users for the last 'days' of days.
        For each user, the total reading time for the specified period is calculated.
        :param days: Number of days from the current date to calculate statistics.
        :return: None
        """
        date_from = timezone.now() - timedelta(days=days)
        for user in User.objects.all():
            total_reading_time = cls.update_reading_stats_for_user(user, date_from)
            UserReadingStats.objects.update_or_create(
                user=user,
                defaults={"statistic_time_" + str(days) + "_days": total_reading_time},
            )


@shared_task
def update_user_reading_stats_7_days():
    UserReadingStatsUpdater.update_user_reading_stats(7)


@shared_task
def update_user_reading_stats_30_days():
    UserReadingStatsUpdater.update_user_reading_stats(30)
