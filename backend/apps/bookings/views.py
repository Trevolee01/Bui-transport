"""
Views for Bookings app
"""
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum
from django.utils import timezone

from .models import Booking, RefundRequest
from .serializers import (
    BookingSerializer, BookingCreateSerializer, BookingUpdateSerializer,
    RefundRequestSerializer, RefundRequestCreateSerializer, RefundRequestUpdateSerializer
)
from .filters import BookingFilter


class BookingListView(generics.ListAPIView):
    """
    List bookings for the current user
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookingFilter
    search_fields = ['transport_option__route_name', 'transport_option__departure_location', 'transport_option__destination']
    ordering_fields = ['booking_date', 'created_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        try:
            student_profile = self.request.user.student_profile
            return Booking.objects.filter(
                student=student_profile
            ).select_related('transport_option', 'transport_option__organizer', 'transport_option__organizer__user')
        except AttributeError:
            return Booking.objects.none()


class BookingDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update a specific booking
    """
    serializer_class = BookingUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        try:
            student_profile = self.request.user.student_profile
            return Booking.objects.filter(student=student_profile)
        except AttributeError:
            return Booking.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookingSerializer
        return BookingUpdateSerializer


class BookingCreateView(generics.CreateAPIView):
    """
    Create a new booking
    """
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Ensure only students can create bookings
        if self.request.user.role != 'student':
            raise PermissionError("Only students can create bookings.")
        
        try:
            student_profile = self.request.user.student_profile
            booking = serializer.save(student=student_profile)
            
            # Update available seats
            transport_option = booking.transport_option
            transport_option.available_seats -= booking.seats_booked
            transport_option.save()
            
        except AttributeError:
            raise PermissionError("Student profile not found.")


class BookingCancelView(generics.UpdateAPIView):
    """
    Cancel a booking
    """
    serializer_class = BookingUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        try:
            student_profile = self.request.user.student_profile
            return Booking.objects.filter(
                student=student_profile,
                booking_status__in=['pending', 'confirmed']
            )
        except AttributeError:
            return Booking.objects.none()
    
    def perform_update(self, serializer):
        booking = self.get_object()
        
        # Update booking status to cancelled
        serializer.save(booking_status='cancelled')
        
        # Refund seats to transport option
        transport_option = booking.transport_option
        transport_option.available_seats += booking.seats_booked
        transport_option.save()
        
        # Update refund status if payment was made
        if booking.payment_status == 'paid':
            booking.refund_status = 'requested'
            booking.refund_amount = booking.total_amount
            booking.save()


class OrganizerBookingListView(generics.ListAPIView):
    """
    List bookings for transport organizer
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookingFilter
    search_fields = ['student__user__first_name', 'student__user__last_name', 'student__student_id']
    ordering_fields = ['booking_date', 'created_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        try:
            organizer = self.request.user.organizer_profile
            return Booking.objects.filter(
                transport_option__organizer=organizer
            ).select_related('student', 'student__user', 'transport_option')
        except AttributeError:
            return Booking.objects.none()


class RefundRequestListView(generics.ListAPIView):
    """
    List refund requests
    """
    serializer_class = RefundRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at', 'refund_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            # Admins can see all refund requests
            return RefundRequest.objects.all().select_related(
                'booking', 'student', 'student__user', 'organizer', 'organizer__user'
            )
        elif self.request.user.role == 'transport_organizer':
            # Organizers can see refund requests for their bookings
            try:
                organizer = self.request.user.organizer_profile
                return RefundRequest.objects.filter(
                    organizer=organizer
                ).select_related('booking', 'student', 'student__user')
            except AttributeError:
                return RefundRequest.objects.none()
        else:
            # Students can see their own refund requests
            try:
                student_profile = self.request.user.student_profile
                return RefundRequest.objects.filter(
                    student=student_profile
                ).select_related('booking', 'organizer', 'organizer__user')
            except AttributeError:
                return RefundRequest.objects.none()


class RefundRequestCreateView(generics.CreateAPIView):
    """
    Create a refund request
    """
    serializer_class = RefundRequestCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Ensure only students can create refund requests
        if self.request.user.role != 'student':
            raise PermissionError("Only students can create refund requests.")
        
        try:
            student_profile = self.request.user.student_profile
            booking = serializer.validated_data['booking']
            organizer = booking.transport_option.organizer
            
            serializer.save(student=student_profile, organizer=organizer)
        except AttributeError:
            raise PermissionError("Student profile not found.")


class RefundRequestDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update a refund request
    """
    serializer_class = RefundRequestUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return RefundRequest.objects.all()
        elif self.request.user.role == 'transport_organizer':
            try:
                organizer = self.request.user.organizer_profile
                return RefundRequest.objects.filter(organizer=organizer)
            except AttributeError:
                return RefundRequest.objects.none()
        else:
            try:
                student_profile = self.request.user.student_profile
                return RefundRequest.objects.filter(student=student_profile)
            except AttributeError:
                return RefundRequest.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RefundRequestSerializer
        elif self.request.user.role == 'admin':
            return RefundRequestUpdateSerializer
        else:
            return RefundRequestSerializer  # Read-only for non-admins


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def booking_stats(request):
    """
    Get booking statistics for the current user
    """
    try:
        if request.user.role == 'student':
            student_profile = request.user.student_profile
            bookings = Booking.objects.filter(student=student_profile)
            
            stats = {
                'total_bookings': bookings.count(),
                'pending_bookings': bookings.filter(booking_status='pending').count(),
                'confirmed_bookings': bookings.filter(booking_status='confirmed').count(),
                'completed_bookings': bookings.filter(booking_status='completed').count(),
                'cancelled_bookings': bookings.filter(booking_status='cancelled').count(),
                'total_spent': bookings.filter(payment_status='paid').aggregate(
                    total=Sum('total_amount')
                )['total'] or 0,
            }
            
        elif request.user.role == 'transport_organizer':
            organizer = request.user.organizer_profile
            bookings = Booking.objects.filter(transport_option__organizer=organizer)
            
            stats = {
                'total_bookings': bookings.count(),
                'pending_bookings': bookings.filter(booking_status='pending').count(),
                'confirmed_bookings': bookings.filter(booking_status='confirmed').count(),
                'completed_bookings': bookings.filter(booking_status='completed').count(),
                'cancelled_bookings': bookings.filter(booking_status='cancelled').count(),
                'total_earnings': bookings.filter(payment_status='paid').aggregate(
                    total=Sum('organizer_amount')
                )['total'] or 0,
                'platform_fees': bookings.filter(payment_status='paid').aggregate(
                    total=Sum('platform_fee')
                )['total'] or 0,
            }
            
        else:
            return Response(
                {'error': 'Invalid user role'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(stats)
        
    except AttributeError:
        return Response(
            {'error': 'Profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )