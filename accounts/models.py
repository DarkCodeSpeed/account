from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

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
    online_time = models.DurationField(default=timedelta)

    def __str__(self):
        return f"{self.user.username}'s profile"
