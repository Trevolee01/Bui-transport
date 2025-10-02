"""
Serializers for Communications app
"""
from rest_framework import serializers
from .models import Conversation, ConversationParticipant, Message, CommunicationReport, Notification
from apps.users.serializers import UserSerializer


class ConversationParticipantSerializer(serializers.ModelSerializer):
    """
    Serializer for conversation participants
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ConversationParticipant
        fields = (
            'id', 'user', 'role', 'joined_at', 'last_read_at', 'is_muted'
        )
        read_only_fields = ('id', 'joined_at')


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for conversations
    """
    participants = ConversationParticipantSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = (
            'id', 'conversation_type', 'trip_id', 'booking_id', 'title',
            'is_active', 'created_by', 'participants', 'last_message',
            'unread_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return {
                'id': str(last_message.id),
                'content': last_message.content[:100] + '...' if len(last_message.content) > 100 else last_message.content,
                'sender': last_message.sender.first_name,
                'created_at': last_message.created_at
            }
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            try:
                participant = obj.participants.get(user=request.user)
                if participant.last_read_at:
                    return obj.messages.filter(created_at__gt=participant.last_read_at).count()
                else:
                    return obj.messages.count()
            except ConversationParticipant.DoesNotExist:
                return 0
        return 0


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for messages
    """
    sender = UserSerializer(read_only=True)
    replied_to = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = (
            'id', 'conversation', 'sender', 'message_type', 'content',
            'media_url', 'location_data', 'is_read', 'replied_to',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'is_read', 'created_at', 'updated_at')
    
    def get_replied_to(self, obj):
        if obj.replied_to:
            return {
                'id': str(obj.replied_to.id),
                'content': obj.replied_to.content[:50] + '...' if len(obj.replied_to.content) > 50 else obj.replied_to.content,
                'sender': obj.replied_to.sender.first_name,
                'created_at': obj.replied_to.created_at
            }
        return None


class MessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating messages
    """
    class Meta:
        model = Message
        fields = (
            'conversation', 'message_type', 'content', 'media_url',
            'location_data', 'replied_to'
        )
    
    def validate_conversation(self, value):
        # Check if user is a participant in the conversation
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if not value.participants.filter(user=request.user).exists():
                raise serializers.ValidationError("You are not a participant in this conversation.")
        return value
    
    def validate_location_data(self, value):
        if value:
            required_keys = ['lat', 'lng']
            if not all(key in value for key in required_keys):
                raise serializers.ValidationError("Location data must contain 'lat' and 'lng' keys.")
            try:
                float(value['lat'])
                float(value['lng'])
            except (ValueError, TypeError):
                raise serializers.ValidationError("Latitude and longitude must be valid numbers.")
        return value


class CommunicationReportSerializer(serializers.ModelSerializer):
    """
    Serializer for communication reports
    """
    reporter = UserSerializer(read_only=True)
    reported_user = UserSerializer(read_only=True)
    reviewed_by = UserSerializer(read_only=True)
    
    class Meta:
        model = CommunicationReport
        fields = (
            'id', 'reporter', 'reported_user', 'message', 'conversation',
            'report_type', 'description', 'status', 'admin_notes',
            'reviewed_by', 'reviewed_at', 'created_at'
        )
        read_only_fields = (
            'id', 'status', 'admin_notes', 'reviewed_by', 'reviewed_at', 'created_at'
        )


class CommunicationReportCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating communication reports
    """
    class Meta:
        model = CommunicationReport
        fields = ('reported_user', 'message', 'conversation', 'report_type', 'description')
    
    def validate(self, attrs):
        # Ensure either message or conversation is provided
        if not attrs.get('message') and not attrs.get('conversation'):
            raise serializers.ValidationError("Either message or conversation must be provided.")
        return attrs


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for notifications
    """
    class Meta:
        model = Notification
        fields = (
            'id', 'title', 'message', 'notification_type', 'related_id',
            'is_read', 'is_push_sent', 'created_at'
        )
        read_only_fields = ('id', 'is_push_sent', 'created_at')


class NotificationUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating notifications
    """
    class Meta:
        model = Notification
        fields = ('is_read',)