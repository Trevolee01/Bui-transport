"""
URLs for Communications app
"""
from django.urls import path
from . import views

urlpatterns = [
    # Conversation endpoints
    path('conversations/', views.ConversationListView.as_view(), name='conversations-list'),
    path('conversations/<uuid:pk>/', views.ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/<uuid:conversation_id>/read/', views.mark_conversation_as_read, name='mark-conversation-read'),
    
    # Message endpoints
    path('conversations/<uuid:conversation_id>/messages/', views.MessageListView.as_view(), name='messages-list'),
    path('messages/<uuid:pk>/', views.MessageDetailView.as_view(), name='message-detail'),
    
    # Communication report endpoints
    path('reports/', views.CommunicationReportListView.as_view(), name='communication-reports-list'),
    path('reports/<uuid:pk>/', views.CommunicationReportDetailView.as_view(), name='communication-report-detail'),
    
    # Notification endpoints
    path('notifications/', views.NotificationListView.as_view(), name='notifications-list'),
    path('notifications/<uuid:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('notifications/mark-all-read/', views.mark_all_notifications_as_read, name='mark-all-notifications-read'),
    path('unread-counts/', views.unread_counts, name='unread-counts'),
]