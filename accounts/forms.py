from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile
import re

INTEREST_CHOICES = [
    ('tech', 'Technology'),
    ('sports', 'Sports'),
    ('music', 'Music'),
    ('travel', 'Travel'),
    ('art', 'Art'),
    ('fitness', 'Fitness'),
    ('food', 'Food & Cooking'),
    ('literature', 'Literature'),
    ('gaming', 'Gaming'),
]

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=15, 
        required=False, 
        error_messages={'invalid': 'Enter a valid phone number.'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your phone number (optional).',
            'class': 'form-control'
        }),
    )
    address = forms.CharField(
        max_length=255, 
        required=False, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your address (optional).',
            'class': 'form-control'
        }),
    )
    birth_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={
            'type': 'date',
            'placeholder': 'Enter your date of birth.',
            'class': 'form-control'
        }),
        help_text='Enter your date of birth.'
    )
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], 
        required=False,
        widget=forms.Select(attrs={
            'placeholder': 'Select your gender (optional).',
            'class': 'form-control'
        }),
        help_text='Select your gender (optional).'
    )
    interests = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES, 
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Select your interests (optional).'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'address', 'birth_date', 'gender', 'interests']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise ValidationError('Enter a valid phone number.')
        return phone

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        if commit:
            user.save()
            # Create or update UserProfile instance
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'phone': self.cleaned_data.get('phone'),
                    'address': self.cleaned_data.get('address'),
                    'birth_date': self.cleaned_data.get('birth_date'),
                    'gender': self.cleaned_data.get('gender'),
                    'interests': ','.join(self.cleaned_data.get('interests', [])),  # Store interests as a comma-separated string
                }
            )
        return user
