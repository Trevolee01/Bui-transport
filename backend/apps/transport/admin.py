"""
Admin configuration for Transport app
"""
from django.contrib import admin
from .models import TransportOption, TripUpdate, Review


@admin.register(TransportOption)
class TransportOptionAdmin(admin.ModelAdmin):
    """
    Transport Option admin
    """
    list_display = ('route_name', 'organizer', 'departure_location', 'destination', 'price', 'available_seats', 'is_active')
    list_filter = ('is_active', 'created_at', 'organizer__approval_status')
    search_fields = ('route_name', 'departure_location', 'destination', 'organizer__business_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Route Information', {'fields': ('organizer', 'route_name', 'departure_location', 'destination')}),
        ('Schedule', {'fields': ('departure_time', 'arrival_time', 'days_of_operation')}),
        ('Pricing & Capacity', {'fields': ('price', 'total_seats', 'available_seats')}),
        ('Status', {'fields': ('is_active',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('organizer', 'organizer__user')


@admin.register(TripUpdate)
class TripUpdateAdmin(admin.ModelAdmin):
    """
    Trip Update admin
    """
    list_display = ('title', 'transport_option', 'organizer', 'update_type', 'is_active', 'created_at')
    list_filter = ('update_type', 'is_active', 'created_at')
    search_fields = ('title', 'message', 'transport_option__route_name', 'organizer__business_name')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Update Information', {'fields': ('transport_option', 'organizer', 'update_type', 'title', 'message')}),
        ('Location & Timing', {'fields': ('location_data', 'estimated_arrival')}),
        ('Status', {'fields': ('is_active',)}),
        ('Timestamp', {'fields': ('created_at',)}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('transport_option', 'organizer', 'organizer__user')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Review admin
    """
    list_display = ('student', 'transport_option', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('student__first_name', 'student__last_name', 'transport_option__route_name', 'comment')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Review Information', {'fields': ('booking', 'student', 'transport_option', 'rating', 'comment')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'transport_option', 'booking')