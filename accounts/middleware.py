from datetime import timedelta
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from accounts.models import UserProfile

class UpdateLoginInfoMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)

            # Get current time and user last login time
            now = timezone.now()
            last_login = request.user.last_login

            # Check if it's a new login session
            if 'last_activity' not in request.session or request.session['last_activity'] != str(last_login):
                # Update last_activity in session to avoid counting multiple times
                request.session['last_activity'] = str(last_login)

                # Only increment login counters if it's a new login
                current_date = now.date()

                # Reset daily login count if it's a new day
                if user_profile.last_login_date != current_date:
                    user_profile.weekly_login_count += user_profile.daily_login_count
                    user_profile.daily_login_count = 0

                # Reset weekly login count if a new week starts
                if (current_date - user_profile.last_login_date).days >= 7:
                    user_profile.monthly_login_count += user_profile.weekly_login_count
                    user_profile.weekly_login_count = 0

                # Reset monthly login count if a new month starts
                if now.month != user_profile.last_login_date.month:
                    user_profile.yearly_login_count += user_profile.monthly_login_count
                    user_profile.monthly_login_count = 0

                # Reset yearly login count if a new year starts
                if now.year != user_profile.last_login_date.year:
                    user_profile.yearly_login_count = 0

                # Increment the login counters only on new login
                user_profile.daily_login_count += 1

                # Update the last login date in user profile
                user_profile.last_login_date = current_date

            # Track and record user online time
            if user_profile.last_activity:
                # Calculate the time difference since the last request and add it to the total online time
                time_diff = now - user_profile.last_activity
                user_profile.online_time += time_diff

            # Update the last activity time to the current request time
            user_profile.last_activity = now
            user_profile.save()
