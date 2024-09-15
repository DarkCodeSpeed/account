from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from .models import UserProfile
from django.utils import timezone
from datetime import date


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()
            print(80 * "*")
            print(f"user: {user}")
            print(80 * "*")


            # Log the user in
            login(request, user)

            # Extract additional information from the form
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            birth_date = form.cleaned_data.get('birth_date')
            gender = form.cleaned_data.get('gender')
            interests = form.cleaned_data.get('interests')

            # Create or update the user's profile
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
                    # Add any other fields here
                }
            )
            # Redirect to a success page or home page
            messages.success(request, 'Your account has been created successfully!')
            return redirect('home')  # Replace 'home' with your desired redirect URL or view

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
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/signin.html', {'form': form})



@login_required
def profile_view(request):
    """Display user profile information."""
    user = request.user  # Get the currently logged-in user
    profile = get_object_or_404(UserProfile, user=user)  # Fetch the UserProfile for the user

    context = {
        'user': user,
        'profile': profile,
        'daily_login_count': profile.daily_login_count,
        'weekly_login_count': profile.weekly_login_count,
        'monthly_login_count': profile.monthly_login_count,
        'yearly_login_count': profile.yearly_login_count,
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required
def logout_view(request):
    """Handles user logout."""
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('signin')


@login_required
def home(request):
    """Render the home page."""
    return render(request, 'home.html')

def calculate_age(birth_date):
    """Calculate the age based on birth_date."""
    if birth_date:
        today = date.today()
        return today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
    return None

