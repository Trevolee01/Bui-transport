"""
Admin configuration for User app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, TransportOrganizer


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin
    """
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('role', 'is_verified', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('role', 'is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """
    Student Profile admin
    """
    list_display = ('user', 'student_id', 'department', 'level', 'is_verified', 'wallet_balance')
    list_filter = ('level', 'department', 'is_verified', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'student_id')
    readonly_fields = ('created_at', 'updated_at', 'verification_date')
    
    fieldsets = (
        ('User Information', {'fields': ('user', 'student_id')}),
        ('Academic Information', {'fields': ('department', 'level')}),
        ('Accommodation', {'fields': ('hostel_name', 'room_number')}),
        ('Emergency Contact', {'fields': ('emergency_contact_name', 'emergency_contact_phone')}),
        ('Verification & Wallet', {'fields': ('is_verified', 'verification_date', 'wallet_balance')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(TransportOrganizer)
class TransportOrganizerAdmin(admin.ModelAdmin):
    """
    Transport Organizer admin
    """
    list_display = ('business_name', 'user', 'approval_status', 'rating', 'total_trips', 'total_earnings')
    list_filter = ('approval_status', 'created_at')
    search_fields = ('business_name', 'user__email', 'user__first_name', 'user__last_name', 'license_number')
    readonly_fields = ('created_at', 'updated_at', 'approval_date', 'rating', 'total_trips', 'total_earnings')
    
    fieldsets = (
        ('User Information', {'fields': ('user', 'business_name')}),
        ('Business Details', {'fields': ('license_number', 'vehicle_count')}),
        ('Banking Information', {'fields': ('bank_account_number', 'bank_name', 'account_holder_name', 'mobile_money_number')}),
        ('Approval Status', {'fields': ('approval_status', 'approval_date', 'approved_by')}),
        ('Statistics', {'fields': ('rating', 'total_trips', 'total_earnings')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'approved_by')