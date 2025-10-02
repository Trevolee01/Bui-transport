"""
Views for Communications app
"""
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone

from .models import Conversation, ConversationParticipant, Message, CommunicationReport, Notification
from .serializers import (
    ConversationSerializer, MessageSerializer, MessageCreateSerializer,
    CommunicationReportSerializer, CommunicationReportCreateSerializer,
    NotificationSerializer, NotificationUpdateSerializer
)


class ConversationListView(generics.ListCreateAPIView):
    """
    List and create conversations
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']
    
    def get_queryset(self):
        return Conversation.objects.filter(
            participants__user=self.request.user,
            is_active=True
        ).prefetch_related('participants', 'participants__user', 'messages').distinct()
    
    def perform_create(self, serializer):
        conversation = serializer.save(created_by=self.request.user)
        # Add creator as participant
        ConversationParticipant.objects.create(
            conversation=conversation,
            user=self.request.user,
            role=self.request.user.role
        )


class ConversationDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update a conversation
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Conversation.objects.filter(
            participants__user=self.request.user
        ).prefetch_related('participants', 'participants__user')


class MessageListView(generics.ListCreateAPIView):
    """
    List and create messages in a conversation
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['created_at']
    
    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__participants__user=self.request.user
        ).select_related('sender', 'replied_to').order_by('created_at')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MessageCreateSerializer
        return MessageSerializer
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a message
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Message.objects.filter(
            conversation__participants__user=self.request.user
        ).select_related('sender', 'conversation')


class CommunicationReportListView(generics.ListCreateAPIView):
    """
    List and create communication reports
    """
    serializer_class = CommunicationReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return CommunicationReport.objects.all().select_related(
                'reporter', 'reported_user', 'message', 'conversation', 'reviewed_by'
            )
        else:
            return CommunicationReport.objects.filter(
                reporter=self.request.user
            ).select_related('reported_user', 'message', 'conversation')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommunicationReportCreateSerializer
        return CommunicationReportSerializer
    
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class CommunicationReportDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update a communication report
    """
    serializer_class = CommunicationReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return CommunicationReport.objects.all()
        else:
            return CommunicationReport.objects.filter(reporter=self.request.user)


class NotificationListView(generics.ListAPIView):
    """
    List notifications for the current user
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update a notification
    """
    serializer_class = NotificationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return NotificationSerializer
        return NotificationUpdateSerializer


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_conversation_as_read(request, conversation_id):
    """
    Mark all messages in a conversation as read
    """
    try:
        conversation = Conversation.objects.get(
            id=conversation_id,
            participants__user=request.user
        )
        
        # Update last_read_at for the participant
        participant = conversation.participants.get(user=request.user)
        participant.last_read_at = timezone.now()
        participant.save()
        
        # Mark messages as read
        Message.objects.filter(
            conversation=conversation,
            created_at__lte=timezone.now()
        ).exclude(sender=request.user).update(is_read=True)
        
        return Response({'message': 'Conversation marked as read'})
    except Conversation.DoesNotExist:
        return Response(
            {'error': 'Conversation not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_as_read(request):
    """
    Mark all notifications as read for the current user
    """
    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)
    
    return Response({'message': 'All notifications marked as read'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_counts(request):
    """
    Get unread counts for conversations and notifications
    """
    # Count unread messages
    unread_messages = Message.objects.filter(
        conversation__participants__user=request.user,
        is_read=False
    ).exclude(sender=request.user).count()
    
    # Count unread notifications
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    return Response({
        'unread_messages': unread_messages,
        'unread_notifications': unread_notifications
    })