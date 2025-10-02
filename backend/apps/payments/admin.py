"""
Admin configuration for Payments app
"""
from django.contrib import admin
from .models import PaymentMethod, Transaction, WalletTransaction, AuditLog


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    """
    Payment Method admin
    """
    list_display = ('student', 'method_type', 'provider_name', 'account_name', 'is_primary', 'is_active')
    list_filter = ('method_type', 'is_primary', 'is_active', 'created_at')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'account_name', 'account_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Payment Method Information', {'fields': ('student', 'method_type', 'provider_name')}),
        ('Account Details', {'fields': ('account_number', 'account_name')}),
        ('Status', {'fields': ('is_primary', 'is_active')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'student__user')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Transaction admin
    """
    list_display = ('payment_reference', 'student', 'transaction_type', 'amount', 'status', 'created_at')
    list_filter = ('transaction_type', 'status', 'payment_method', 'created_at')
    search_fields = ('payment_reference', 'external_reference', 'student__user__first_name', 'description')
    readonly_fields = ('created_at', 'processed_at')
    
    fieldsets = (
        ('Transaction Information', {'fields': ('booking', 'student', 'organizer', 'transaction_type', 'amount', 'currency')}),
        ('Payment Details', {'fields': ('payment_method', 'payment_reference', 'external_reference', 'status')}),
        ('Gateway Response', {'fields': ('gateway_response', 'processed_at')}),
        ('Additional Information', {'fields': ('description',)}),
        ('Timestamp', {'fields': ('created_at',)}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'student', 'student__user', 'organizer', 'organizer__user', 'booking'
        )


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    """
    Wallet Transaction admin
    """
    list_display = ('student', 'transaction_type', 'amount', 'balance_before', 'balance_after', 'created_at')
    list_filter = ('transaction_type', 'reference_type', 'created_at')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'description')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Wallet Transaction Information', {'fields': ('student', 'transaction_type', 'amount')}),
        ('Balance Information', {'fields': ('balance_before', 'balance_after')}),
        ('Reference Information', {'fields': ('reference_type', 'reference_id', 'description')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'student__user')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Audit Log admin
    """
    list_display = ('action', 'user', 'table_name', 'record_id', 'created_at')
    list_filter = ('action', 'table_name', 'created_at')
    search_fields = ('action', 'user__first_name', 'user__last_name', 'table_name')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Audit Information', {'fields': ('user', 'action', 'table_name', 'record_id')}),
        ('Changes', {'fields': ('old_values', 'new_values')}),
        ('Request Information', {'fields': ('ip_address', 'user_agent')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def has_add_permission(self, request):
        return False  # Audit logs should only be created programmatically