from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('update-online-time/', views.update_online_time_view, name='update_online_time'),
]

# urlpatterns = [
#     # Your other URL patterns
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
