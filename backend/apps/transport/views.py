"""
Views for Transport app
"""
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg
from django.utils import timezone

from .models import TransportOption, TripUpdate, Review
from .serializers import (
    TransportOptionSerializer, TransportOptionCreateSerializer,
    TripUpdateSerializer, TripUpdateCreateSerializer,
    ReviewSerializer, ReviewCreateSerializer
)
from .filters import TransportOptionFilter


class TransportOptionListView(generics.ListAPIView):
    """
    List all active transport options with filtering
    """
    serializer_class = TransportOptionSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TransportOptionFilter
    search_fields = ['route_name', 'departure_location', 'destination']
    ordering_fields = ['price', 'departure_time', 'created_at']
    ordering = ['departure_time']
    
    def get_queryset(self):
        return TransportOption.objects.filter(
            is_active=True,
            organizer__approval_status='approved'
        ).select_related('organizer', 'organizer__user').prefetch_related('reviews')


class TransportOptionDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific transport option
    """
    serializer_class = TransportOptionSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return TransportOption.objects.filter(
            is_active=True,
            organizer__approval_status='approved'
        ).select_related('organizer', 'organizer__user').prefetch_related('reviews')


class TransportOptionCreateView(generics.CreateAPIView):
    """
    Create a new transport option (for organizers)
    """
    serializer_class = TransportOptionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Get the organizer profile for the current user
        try:
            organizer = self.request.user.organizer_profile
            if organizer.approval_status != 'approved':
                raise PermissionError("Only approved organizers can create transport options.")
            serializer.save(organizer=organizer)
        except AttributeError:
            raise PermissionError("Only transport organizers can create transport options.")


class TransportOptionUpdateView(generics.UpdateAPIView):
    """
    Update transport option (for organizers)
    """
    serializer_class = TransportOptionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TransportOption.objects.filter(organizer__user=self.request.user)


class TransportOptionDeleteView(generics.DestroyAPIView):
    """
    Delete transport option (for organizers)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return TransportOption.objects.filter(organizer__user=self.request.user)


class OrganizerTransportOptionsView(generics.ListAPIView):
    """
    List transport options for a specific organizer
    """
    serializer_class = TransportOptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        organizer_id = self.kwargs.get('organizer_id')
        if organizer_id:
            return TransportOption.objects.filter(
                organizer_id=organizer_id,
                organizer__approval_status='approved'
            ).select_related('organizer', 'organizer__user')
        else:
            # Return current user's transport options
            try:
                organizer = self.request.user.organizer_profile
                return TransportOption.objects.filter(organizer=organizer)
            except AttributeError:
                return TransportOption.objects.none()


class TripUpdateListView(generics.ListAPIView):
    """
    List trip updates for a transport option
    """
    serializer_class = TripUpdateSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        transport_option_id = self.kwargs.get('transport_option_id')
        return TripUpdate.objects.filter(
            transport_option_id=transport_option_id,
            is_active=True
        ).select_related('organizer', 'organizer__user', 'transport_option')


class TripUpdateCreateView(generics.CreateAPIView):
    """
    Create trip update (for organizers)
    """
    serializer_class = TripUpdateCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Get the organizer profile for the current user
        try:
            organizer = self.request.user.organizer_profile
            if organizer.approval_status != 'approved':
                raise PermissionError("Only approved organizers can create trip updates.")
            serializer.save(organizer=organizer)
        except AttributeError:
            raise PermissionError("Only transport organizers can create trip updates.")


class ReviewListView(generics.ListAPIView):
    """
    List reviews for a transport option
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        transport_option_id = self.kwargs.get('transport_option_id')
        return Review.objects.filter(
            transport_option_id=transport_option_id
        ).select_related('student', 'transport_option', 'booking')


class ReviewCreateView(generics.CreateAPIView):
    """
    Create a review (for students)
    """
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Ensure only students can create reviews
        if self.request.user.role != 'student':
            raise PermissionError("Only students can create reviews.")
        serializer.save(student=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a review
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(student=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def transport_option_stats(request, pk):
    """
    Get statistics for a transport option
    """
    try:
        transport_option = TransportOption.objects.get(pk=pk)
        
        # Calculate average rating
        avg_rating = Review.objects.filter(
            transport_option=transport_option
        ).aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        
        # Count total reviews
        total_reviews = Review.objects.filter(transport_option=transport_option).count()
        
        # Count total bookings
        total_bookings = transport_option.bookings.filter(
            booking_status='completed'
        ).count()
        
        return Response({
            'transport_option_id': str(transport_option.id),
            'route_name': transport_option.route_name,
            'average_rating': round(avg_rating, 2),
            'total_reviews': total_reviews,
            'total_bookings': total_bookings,
            'occupancy_rate': round((transport_option.total_seats - transport_option.available_seats) / transport_option.total_seats * 100, 2) if transport_option.total_seats > 0 else 0
        })
    except TransportOption.DoesNotExist:
        return Response(
            {'error': 'Transport option not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )