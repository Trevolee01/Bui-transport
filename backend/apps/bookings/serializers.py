"""
Serializers for Bookings app
"""
from rest_framework import serializers
from django.utils import timezone
from .models import Booking, RefundRequest
from apps.users.serializers import StudentProfileSerializer
from apps.transport.serializers import TransportOptionSerializer


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for bookings
    """
    student = StudentProfileSerializer(read_only=True)
    transport_option = TransportOptionSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = (
            'id', 'student', 'transport_option', 'booking_date', 'seats_booked',
            'total_amount', 'platform_fee', 'organizer_amount', 'booking_status',
            'payment_status', 'payment_method', 'payment_reference', 'refund_amount',
            'refund_status', 'refund_reason', 'special_requests', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'total_amount', 'platform_fee', 'organizer_amount', 
            'payment_reference', 'refund_amount', 'refund_status', 'created_at', 'updated_at'
        )


class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating bookings
    """
    class Meta:
        model = Booking
        fields = (
            'transport_option', 'booking_date', 'seats_booked', 
            'payment_method', 'special_requests'
        )
    
    def validate_booking_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Booking date cannot be in the past.")
        return value
    
    def validate_seats_booked(self, value):
        if value <= 0:
            raise serializers.ValidationError("Number of seats must be greater than 0.")
        return value
    
    def validate(self, attrs):
        transport_option = attrs['transport_option']
        seats_booked = attrs['seats_booked']
        
        # Check if transport option is active
        if not transport_option.is_active:
            raise serializers.ValidationError("This transport option is not available.")
        
        # Check if organizer is approved
        if transport_option.organizer.approval_status != 'approved':
            raise serializers.ValidationError("This transport option is not available.")
        
        # Check seat availability
        if seats_booked > transport_option.available_seats:
            raise serializers.ValidationError(
                f"Only {transport_option.available_seats} seats available."
            )
        
        # Check if booking date is valid for the transport option
        booking_date = attrs['booking_date']
        day_name = booking_date.strftime('%A').lower()
        if day_name not in transport_option.days_of_operation:
            raise serializers.ValidationError(
                f"This transport option does not operate on {day_name}."
            )
        
        return attrs


class BookingUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating bookings
    """
    class Meta:
        model = Booking
        fields = ('booking_status', 'payment_status', 'special_requests')
    
    def validate_booking_status(self, value):
        # Only allow certain status transitions
        allowed_transitions = {
            'pending': ['confirmed', 'cancelled'],
            'confirmed': ['cancelled', 'completed'],
            'cancelled': [],
            'completed': []
        }
        
        # Get current booking status
        if self.instance:
            current_status = self.instance.booking_status
            if value not in allowed_transitions.get(current_status, []):
                raise serializers.ValidationError(
                    f"Cannot change status from {current_status} to {value}."
                )
        
        return value


class RefundRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for refund requests
    """
    booking = BookingSerializer(read_only=True)
    student = StudentProfileSerializer(read_only=True)
    processed_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = RefundRequest
        fields = (
            'id', 'booking', 'student', 'organizer', 'refund_amount', 'reason',
            'status', 'admin_notes', 'processed_by', 'processed_at', 'created_at'
        )
        read_only_fields = (
            'id', 'status', 'admin_notes', 'processed_by', 'processed_at', 'created_at'
        )


class RefundRequestCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating refund requests
    """
    class Meta:
        model = RefundRequest
        fields = ('booking', 'refund_amount', 'reason')
    
    def validate_booking(self, value):
        # Check if booking belongs to the current user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            try:
                student_profile = request.user.student_profile
                if value.student != student_profile:
                    raise serializers.ValidationError("You can only request refunds for your own bookings.")
            except AttributeError:
                raise serializers.ValidationError("Student profile not found.")
        
        # Check if booking is eligible for refund
        if value.booking_status not in ['confirmed', 'completed']:
            raise serializers.ValidationError("Only confirmed or completed bookings can be refunded.")
        
        # Check if refund already exists
        if RefundRequest.objects.filter(booking=value).exists():
            raise serializers.ValidationError("Refund request already exists for this booking.")
        
        return value
    
    def validate_refund_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Refund amount must be greater than 0.")
        return value


class RefundRequestUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating refund requests (admin only)
    """
    class Meta:
        model = RefundRequest
        fields = ('status', 'admin_notes')
    
    def validate_status(self, value):
        # Only allow certain status transitions
        allowed_transitions = {
            'pending': ['approved', 'rejected'],
            'approved': ['processed'],
            'rejected': [],
            'processed': []
        }
        
        # Get current status
        if self.instance:
            current_status = self.instance.status
            if value not in allowed_transitions.get(current_status, []):
                raise serializers.ValidationError(
                    f"Cannot change status from {current_status} to {value}."
                )
        
        return value