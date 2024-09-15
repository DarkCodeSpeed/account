from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from .models import UserProfile
from django.utils import timezone
from datetime import date, timedelta

def format_online_time(seconds):
    """Format online time in hours:minutes:seconds format."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def update_online_time(user_profile):
    now = timezone.now()
    if user_profile.last_activity:
        time_diff = now - user_profile.last_activity
        user_profile.online_time += time_diff
    user_profile.last_activity = now
    user_profile.save()

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            birth_date = form.cleaned_data.get('birth_date')
            gender = form.cleaned_data.get('gender')
            interests = form.cleaned_data.get('interests')

            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone': phone,
                    'address': address,
                    'birth_date': birth_date,
                    'gender': gender,
                    'interests': interests,
                    'age': calculate_age(birth_date),
                }
            )
            messages.success(request, 'Your account has been created successfully!')
            return redirect('home')

    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def signin(request):
    """Handles user sign-in."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            user_profile, created = UserProfile.objects.get_or_create(user=user)
            update_online_time(user_profile)

            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/signin.html', {'form': form})

def profile_view(request):
    """Display user profile information."""
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    online_time = profile.online_time.total_seconds() if profile.online_time else 0
    formatted_online_time = format_online_time(online_time)

    context = {
        'user': user,
        'profile': profile,
        'daily_login_count': profile.daily_login_count,
        'weekly_login_count': profile.weekly_login_count,
        'monthly_login_count': profile.monthly_login_count,
        'yearly_login_count': profile.yearly_login_count,
        'online_time': formatted_online_time
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def logout_view(request):
    """Handles user logout."""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    update_online_time(user_profile)

    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('signin')

@login_required
def home(request):
    """Render the home page."""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    update_online_time(user_profile)
    return render(request, 'home.html')

def calculate_age(birth_date):
    """Calculate the age based on birth_date."""
    if birth_date:
        today = date.today()
        return today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
    return None

@login_required
def update_online_time_view(request):
    """Update the user's online time via AJAX."""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    update_online_time(user_profile)
    online_time_seconds = user_profile.online_time.total_seconds() if user_profile.online_time else 0
    return JsonResponse({
        'status': 'success',
        'online_time': format_online_time(online_time_seconds)
    })
