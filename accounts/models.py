from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    first_join = models.DateTimeField(auto_now_add=True)
    last_join = models.DateTimeField(default=timezone.now)
    age = models.PositiveIntegerField(blank=True, null=True)

    # Login count tracking
    daily_login_count = models.IntegerField(default=0)
    weekly_login_count = models.IntegerField(default=0)
    monthly_login_count = models.IntegerField(default=0)
    yearly_login_count = models.IntegerField(default=0)

    # To track when the counts were last reset
    last_login_date = models.DateField(auto_now=True)

    # Online time tracking fields
    last_activity = models.DateTimeField(null=True, blank=True)
    online_time = models.DurationField(default=timedelta(0))

    def update_online_time(self):
        """Updates the online time based on the last activity."""
        if self.last_activity:
            current_time = timezone.now()
            time_spent = current_time - self.last_activity
            self.online_time += time_spent
            self.save(update_fields=['online_time'])
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])

    def __str__(self):
        return f"{self.user.username}'s profile"

    def reset_login_counts(self):
        """Resets the login counts based on the period (daily, weekly, etc.)."""
        now = timezone.now().date()

        if now > self.last_login_date:
            # Reset daily login count if needed
            if now > self.last_login_date:
                self.daily_login_count = 0
            # Reset weekly login count if the current week is different
            if now.isocalendar()[1] != self.last_login_date.isocalendar()[1]:
                self.weekly_login_count = 0
            # Reset monthly login count if the current month is different
            if now.month != self.last_login_date.month:
                self.monthly_login_count = 0
            # Reset yearly login count if the current year is different
            if now.year != self.last_login_date.year:
                self.yearly_login_count = 0

            self.save(update_fields=[
                'daily_login_count', 'weekly_login_count',
                'monthly_login_count', 'yearly_login_count', 'last_login_date'
            ])


class OnlineUserActivity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_activity = models.DateTimeField()

    @staticmethod
    def update_user_activity(user):
        """Updates the timestamp for the user's last action."""
        OnlineUserActivity.objects.update_or_create(user=user, defaults={'last_activity': timezone.now()})

    @staticmethod
    def get_user_activities(time_delta=timedelta(minutes=15)):
        """
        Gathers OnlineUserActivity objects from the database representing active users.

        :param time_delta: The amount of time in the past to classify a user as "active". Default is 15 minutes.
        :return: QuerySet of active users within the time_delta
        """
        starting_time = timezone.now() - time_delta
        return OnlineUserActivity.objects.filter(last_activity__gte=starting_time).order_by('-last_activity')
