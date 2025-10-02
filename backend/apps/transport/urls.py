"""
URLs for Transport app
"""
from django.urls import path
from . import views

urlpatterns = [
    # Transport options endpoints
    path('options/', views.TransportOptionListView.as_view(), name='transport-options-list'),
    path('options/<uuid:pk>/', views.TransportOptionDetailView.as_view(), name='transport-option-detail'),
    path('options/create/', views.TransportOptionCreateView.as_view(), name='transport-option-create'),
    path('options/<uuid:pk>/update/', views.TransportOptionUpdateView.as_view(), name='transport-option-update'),
    path('options/<uuid:pk>/delete/', views.TransportOptionDeleteView.as_view(), name='transport-option-delete'),
    path('options/<uuid:pk>/stats/', views.transport_option_stats, name='transport-option-stats'),
    
    # Organizer transport options
    path('organizer/<uuid:organizer_id>/options/', views.OrganizerTransportOptionsView.as_view(), name='organizer-transport-options'),
    path('my-options/', views.OrganizerTransportOptionsView.as_view(), name='my-transport-options'),
    
    # Trip updates endpoints
    path('options/<uuid:transport_option_id>/updates/', views.TripUpdateListView.as_view(), name='trip-updates-list'),
    path('updates/create/', views.TripUpdateCreateView.as_view(), name='trip-update-create'),
    
    # Reviews endpoints
    path('options/<uuid:transport_option_id>/reviews/', views.ReviewListView.as_view(), name='reviews-list'),
    path('reviews/create/', views.ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<uuid:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
]