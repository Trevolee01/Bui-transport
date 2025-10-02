"""
Filters for Bookings app
"""
import django_filters
from .models import Booking, RefundRequest


class BookingFilter(django_filters.FilterSet):
    """
    Filter for bookings
    """
    booking_status = django_filters.ChoiceFilter(choices=Booking.BOOKING_STATUS_CHOICES)
    payment_status = django_filters.ChoiceFilter(choices=Booking.PAYMENT_STATUS_CHOICES)
    payment_method = django_filters.ChoiceFilter(choices=Booking.PAYMENT_METHOD_CHOICES)
    booking_date_after = django_filters.DateFilter(field_name='booking_date', lookup_expr='gte')
    booking_date_before = django_filters.DateFilter(field_name='booking_date', lookup_expr='lte')
    min_amount = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Booking
        fields = [
            'booking_status', 'payment_status', 'payment_method',
            'booking_date_after', 'booking_date_before', 'min_amount', 'max_amount',
            'created_after', 'created_before'
        ]


class RefundRequestFilter(django_filters.FilterSet):
    """
    Filter for refund requests
    """
    status = django_filters.ChoiceFilter(choices=RefundRequest.REFUND_STATUS_CHOICES)
    min_amount = django_filters.NumberFilter(field_name='refund_amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='refund_amount', lookup_expr='lte')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = RefundRequest
        fields = [
            'status', 'min_amount', 'max_amount', 'created_after', 'created_before'
        ]