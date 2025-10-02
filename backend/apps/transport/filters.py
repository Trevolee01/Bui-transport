"""
Filters for Transport app
"""
import django_filters
from .models import TransportOption


class TransportOptionFilter(django_filters.FilterSet):
    """
    Filter for transport options
    """
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    departure_location = django_filters.CharFilter(field_name='departure_location', lookup_expr='icontains')
    destination = django_filters.CharFilter(field_name='destination', lookup_expr='icontains')
    departure_time_after = django_filters.TimeFilter(field_name='departure_time', lookup_expr='gte')
    departure_time_before = django_filters.TimeFilter(field_name='departure_time', lookup_expr='lte')
    days_of_operation = django_filters.CharFilter(method='filter_days_of_operation')
    min_available_seats = django_filters.NumberFilter(field_name='available_seats', lookup_expr='gte')
    
    class Meta:
        model = TransportOption
        fields = [
            'min_price', 'max_price', 'departure_location', 'destination',
            'departure_time_after', 'departure_time_before', 'days_of_operation',
            'min_available_seats'
        ]
    
    def filter_days_of_operation(self, queryset, name, value):
        """
        Filter by days of operation
        """
        if value:
            # Split comma-separated days
            days = [day.strip() for day in value.split(',')]
            # Filter transport options that operate on any of the specified days
            return queryset.filter(days_of_operation__overlap=days)
        return queryset