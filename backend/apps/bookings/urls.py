"""
URLs for Bookings app
"""
from django.urls import path
from . import views

urlpatterns = [
    # Booking endpoints
    path('', views.BookingListView.as_view(), name='bookings-list'),
    path('create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('<uuid:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('<uuid:pk>/cancel/', views.BookingCancelView.as_view(), name='booking-cancel'),
    path('stats/', views.booking_stats, name='booking-stats'),
    
    # Organizer booking endpoints
    path('organizer/', views.OrganizerBookingListView.as_view(), name='organizer-bookings'),
    
    # Refund request endpoints
    path('refunds/', views.RefundRequestListView.as_view(), name='refund-requests-list'),
    path('refunds/create/', views.RefundRequestCreateView.as_view(), name='refund-request-create'),
    path('refunds/<uuid:pk>/', views.RefundRequestDetailView.as_view(), name='refund-request-detail'),
]