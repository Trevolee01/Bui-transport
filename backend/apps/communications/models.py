"""
Communication models for BUI Transport System
"""
import uuid
from django.db import models
from apps.users.models import User


class Conversation(models.Model):
    """
    Conversations between users
    """
    CONVERSATION_TYPE_CHOICES = [
        ('direct', 'Direct Message'),
        ('trip_group', 'Trip Group'),
        ('support', 'Support'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_type = models.CharField(max_length=20, choices=CONVERSATION_TYPE_CHOICES)
    trip_id = models.UUIDField(blank=True, null=True, help_text="For trip-specific conversations")
    booking_id = models.UUIDField(blank=True, null=True, help_text="For booking-specific conversations")
    title = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversations'
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.get_conversation_type_display()} - {self.title or 'Untitled'}"


class ConversationParticipant(models.Model):
    """
    Participants in conversations
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('organizer', 'Organizer'),
        ('student', 'Student'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation_participants')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_read_at = models.DateTimeField(blank=True, null=True)
    is_muted = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'conversation_participants'
        verbose_name = 'Conversation Participant'
        verbose_name_plural = 'Conversation Participants'
        unique_together = ['conversation', 'user']
    
    def __str__(self):
        return f"{self.user.first_name} in {self.conversation}"


class Message(models.Model):
    """
    Messages in conversations
    """
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('location', 'Location'),
        ('announcement', 'Announcement'),
        ('system', 'System'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text')
    content = models.TextField()
    media_url = models.URLField(blank=True, null=True, max_length=500)
    location_data = models.JSONField(
        blank=True, 
        null=True, 
        help_text="GPS coordinates: {'lat': 6.5244, 'lng': 3.3792}"
    )
    is_read = models.BooleanField(default=False)
    replied_to = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.first_name}: {self.content[:50]}..."


class CommunicationReport(models.Model):
    """
    Reports for inappropriate communication
    """
    REPORT_TYPE_CHOICES = [
        ('spam', 'Spam'),
        ('harassment', 'Harassment'),
        ('inappropriate_content', 'Inappropriate Content'),
        ('fraud', 'Fraud'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='communication_reports')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_communications')
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=30, choices=REPORT_TYPE_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reviewed_communications'
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'communication_reports'
        verbose_name = 'Communication Report'
        verbose_name_plural = 'Communication Reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report by {self.reporter.first_name} - {self.get_report_type_display()}"


class Notification(models.Model):
    """
    System notifications for users
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('booking', 'Booking'),
        ('payment', 'Payment'),
        ('trip_update', 'Trip Update'),
        ('message', 'Message'),
        ('approval', 'Approval'),
        ('reminder', 'Reminder'),
        ('general', 'General'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    related_id = models.UUIDField(blank=True, null=True, help_text="ID of related object (booking, message, etc.)")
    is_read = models.BooleanField(default=False)
    is_push_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.first_name} - {self.title}"