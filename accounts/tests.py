# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import get_user_model

# from django.utils import timezone
# from django.contrib.auth import login
# from django.contrib.messages import get_messages
# from .models import UserProfile
# from .forms import CustomUserCreationForm

# class SigninTests(TestCase):
#     def setUp(self):
#         self.username = 'testuser'
#         self.password = '12345'
#         self.user = User.objects.create_user(username=self.username, password=self.password)

#     def test_signin_invalid_user(self):
#         response = self.client.post(reverse('signin'), {
#             'username': 'wronguser',
#             'password': 'wrongpassword',
#         })
#         self.assertContains(response, 'Please enter a correct username and password.')

#     def test_signin_valid_user(self):
#         response = self.client.post(reverse('signin'), {
#             'username': self.username,
#             'password': self.password,
#         })
#         self.assertRedirects(response, reverse('home'))
#         self.assertIn('_auth_user_id', self.client.session)  # Check if user is logged in

#     def test_signin_form_display(self):
#         response = self.client.get(reverse('signin'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'accounts/signin.html')
#         self.assertContains(response, 'Sign In')
#         self.assertContains(response, '<form method="post">')
# views.py


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .forms import CustomUserCreationForm
from .models import UserProfile

User = get_user_model()

class SignupTests(TestCase):
    
    def setUp(self):
        """Create a user instance for use in tests."""
        self.valid_user_data = {
            'username': 'newuser',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
            'email': 'newuser@example.com',
            'phone': '1234567890',
            'address': '123 Test Street',
            'birth_date': '1990-01-01',
            'gender': 'M',
            'interests': ['coding', 'reading']
        }
        self.existing_user = User.objects.create_user(
            username='existinguser', 
            password='password'
        )
        
    def test_signup_valid_user(self):
        """Test that a user can sign up with valid data."""
        response = self.client.post(reverse('signup'), self.valid_user_data)
        
        # Check that the user is created
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')
        
        # Check that the user is logged in
        self.assertEqual(response.status_code, 302)  # Redirect to home page
        
        # Check the UserProfile creation
        profile = UserProfile.objects.get(user__username='newuser')
        self.assertEqual(profile.phone, '1234567890')
        self.assertEqual(profile.address, '123 Test Street')
        self.assertEqual(profile.gender, 'M')
        self.assertEqual(profile.interests, 'coding,reading')
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Account created and logged in successfully!")
    
    def test_signup_invalid_user(self):
        """Test that invalid user data shows form errors."""
        invalid_data = self.valid_user_data.copy()
        invalid_data['password2'] = 'mismatchpassword'  # Passwords do not match
        
        response = self.client.post(reverse('signup'), invalid_data)
        
        # Check that the form is returned with errors
        form = response.context.get('form')
        self.assertIsNotNone(form, "Form is not in the response context.")
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')
    
    def test_signup_existing_user(self):
        """Test that an error is shown when trying to sign up with an existing username."""
        existing_user_data = self.valid_user_data.copy()
        existing_user_data['username'] = 'existinguser'  # Username already exists
        
        response = self.client.post(reverse('signup'), existing_user_data)
        
        # Check that form shows error
        form = response.context.get('form')
        self.assertIsNotNone(form, "Form is not in the response context.")
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')

        # Check that the user count has not increased
        self.assertEqual(User.objects.count(), 1)  # Only the existing user should be present
