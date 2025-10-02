"""
Admin configuration for Communications app
"""
from django.contrib import admin
from .models import Conversation, ConversationParticipant, Message, CommunicationReport, Notification


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """
    Conversation admin
    """
    list_display = ('title', 'conversation_type', 'created_by', 'is_active', 'created_at')
    list_filter = ('conversation_type', 'is_active', 'created_at')
    search_fields = ('title', 'created_by__first_name', 'created_by__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Conversation Information', {'fields': ('conversation_type', 'trip_id', 'booking_id', 'title')}),
        ('Status', {'fields': ('is_active',)}),
        ('Creator', {'fields': ('created_by',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')


@admin.register(ConversationParticipant)
class ConversationParticipantAdmin(admin.ModelAdmin):
    """
    Conversation Participant admin
    """
    list_display = ('user', 'conversation', 'role', 'joined_at', 'is_muted')
    list_filter = ('role', 'is_muted', 'joined_at')
    search_fields = ('user__first_name', 'user__last_name', 'conversation__title')
    
    fieldsets = (
        ('Participant Information', {'fields': ('conversation', 'user', 'role')}),
        ('Status', {'fields': ('is_muted', 'last_read_at')}),
        ('Timestamp', {'fields': ('joined_at',)}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'conversation')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Message admin
    """
    list_display = ('sender', 'conversation', 'message_type', 'is_read', 'created_at')
    list_filter = ('message_type', 'is_read', 'created_at')
    search_fields = ('content', 'sender__first_name', 'sender__last_name', 'conversation__title')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Message Information', {'fields': ('conversation', 'sender', 'message_type', 'content')}),
        ('Media & Location', {'fields': ('media_url', 'location_data')}),
        ('Status', {'fields': ('is_read', 'replied_to')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sender', 'conversation', 'replied_to')


@admin.register(CommunicationReport)
class CommunicationReportAdmin(admin.ModelAdmin):
    """
    Communication Report admin
    """
    list_display = ('reporter', 'reported_user', 'report_type', 'status', 'created_at')
    list_filter = ('report_type', 'status', 'created_at')
    search_fields = ('description', 'reporter__first_name', 'reported_user__first_name')
    readonly_fields = ('created_at', 'reviewed_at')
    
    fieldsets = (
        ('Report Information', {'fields': ('reporter', 'reported_user', 'message', 'conversation')}),
        ('Report Details', {'fields': ('report_type', 'description')}),
        ('Review', {'fields': ('status', 'admin_notes', 'reviewed_by', 'reviewed_at')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'reporter', 'reported_user', 'message', 'conversation', 'reviewed_by'
        )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Notification admin
    """
    list_display = ('user', 'title', 'notification_type', 'is_read', 'is_push_sent', 'created_at')
    list_filter = ('notification_type', 'is_read', 'is_push_sent', 'created_at')
    search_fields = ('title', 'message', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Notification Information', {'fields': ('user', 'title', 'message', 'notification_type', 'related_id')}),
        ('Status', {'fields': ('is_read', 'is_push_sent')}),
        ('Timestamp', {'fields': ('created_at',)}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')