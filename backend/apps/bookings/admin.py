"""
Admin configuration for Bookings app
"""
from django.contrib import admin
from .models import Booking, RefundRequest


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Booking admin
    """
    list_display = ('student', 'transport_option', 'booking_date', 'seats_booked', 'total_amount', 'booking_status', 'payment_status')
    list_filter = ('booking_status', 'payment_status', 'payment_method', 'booking_date', 'created_at')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'student__student_id', 'transport_option__route_name')
    readonly_fields = ('created_at', 'updated_at', 'payment_reference')
    
    fieldsets = (
        ('Booking Information', {'fields': ('student', 'transport_option', 'booking_date', 'seats_booked')}),
        ('Payment Information', {'fields': ('total_amount', 'platform_fee', 'organizer_amount', 'payment_method', 'payment_reference', 'payment_status')}),
        ('Status', {'fields': ('booking_status', 'refund_status', 'refund_amount', 'refund_reason')}),
        ('Additional Information', {'fields': ('special_requests',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'student', 'student__user', 'transport_option', 'transport_option__organizer'
        )


@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    """
    Refund Request admin
    """
    list_display = ('booking', 'student', 'organizer', 'refund_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('booking__student__user__first_name', 'booking__student__user__last_name', 'reason')
    readonly_fields = ('created_at', 'processed_at')
    
    fieldsets = (
        ('Refund Information', {'fields': ('booking', 'student', 'organizer', 'refund_amount', 'reason')}),
        ('Processing', {'fields': ('status', 'admin_notes', 'processed_by', 'processed_at')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'booking', 'student', 'student__user', 'organizer', 'organizer__user', 'processed_by'
        )