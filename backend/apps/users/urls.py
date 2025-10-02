"""
URLs for User app
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.logout_view, name='user-logout'),
    
    # User profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    
    # Student profile endpoints
    path('student/profile/', views.StudentProfileView.as_view(), name='student-profile'),
    path('student/profile/create/', views.StudentProfileCreateView.as_view(), name='student-profile-create'),
    
    # Transport organizer profile endpoints
    path('organizer/profile/', views.TransportOrganizerProfileView.as_view(), name='organizer-profile'),
    path('organizer/profile/create/', views.TransportOrganizerCreateView.as_view(), name='organizer-profile-create'),
]