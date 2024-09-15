from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserProfile

# Create a profile when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Save the profile whenever a user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# Update last_join when the user logs in
from django.contrib.auth.signals import user_logged_in

@receiver(user_logged_in)
def update_last_join(sender, request, user, **kwargs):
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.last_join = timezone.now()
    profile.save()
