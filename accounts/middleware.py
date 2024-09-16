from datetime import timedelta
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from accounts.models import UserProfile
from .models import OnlineUserActivity  # Correct import path


class UpdateLoginInfoMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)

            now = timezone.now()
            last_login = request.user.last_login

            if 'last_activity' not in request.session or request.session['last_activity'] != str(last_login):
                request.session['last_activity'] = str(last_login)

                current_date = now.date()

                # Reset daily login count if it's a new day
                if user_profile.last_login_date != current_date:
                    user_profile.weekly_login_count += user_profile.daily_login_count
                    user_profile.daily_login_count = 0

                # Reset weekly login count if 7 days have passed
                if (current_date - user_profile.last_login_date).days >= 7:
                    user_profile.monthly_login_count += user_profile.weekly_login_count
                    user_profile.weekly_login_count = 0

                # Reset monthly login count if it's a new month
                if now.month != user_profile.last_login_date.month:
                    user_profile.yearly_login_count += user_profile.monthly_login_count
                    user_profile.monthly_login_count = 0

                # Reset yearly login count if it's a new year
                if now.year != user_profile.last_login_date.year:
                    user_profile.yearly_login_count = 0

                # Increment daily login count
                user_profile.daily_login_count += 1
                user_profile.last_login_date = current_date

            # Calculate online time
            if user_profile.last_activity:
                time_diff = now - user_profile.last_activity
                user_profile.online_time += time_diff

            # Update last activity timestamp
            user_profile.last_activity = now
            user_profile.save()


class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            OnlineUserActivity.update_user_activity(request.user)
            request.user.userprofile.update_online_time()  # Update online time for the profile
        return self.get_response(request)
