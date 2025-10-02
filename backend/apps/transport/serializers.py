"""
Serializers for Transport app
"""
from rest_framework import serializers
from .models import TransportOption, TripUpdate, Review
from apps.users.serializers import UserSerializer, TransportOrganizerSerializer


class TransportOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for transport options
    """
    organizer = TransportOrganizerSerializer(read_only=True)
    organizer_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = TransportOption
        fields = (
            'id', 'organizer', 'organizer_id', 'route_name', 'departure_location',
            'destination', 'departure_time', 'arrival_time', 'price', 'total_seats',
            'available_seats', 'days_of_operation', 'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'available_seats')
    
    def validate_organizer_id(self, value):
        from apps.users.models import TransportOrganizer
        try:
            organizer = TransportOrganizer.objects.get(id=value)
            if organizer.approval_status != 'approved':
                raise serializers.ValidationError("Only approved organizers can create transport options.")
            return value
        except TransportOrganizer.DoesNotExist:
            raise serializers.ValidationError("Invalid organizer ID.")
    
    def validate_days_of_operation(self, value):
        valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if not isinstance(value, list):
            raise serializers.ValidationError("Days of operation must be a list.")
        for day in value:
            if day not in valid_days:
                raise serializers.ValidationError(f"Invalid day: {day}. Must be one of {valid_days}")
        return value
    
    def validate(self, attrs):
        if attrs['departure_time'] >= attrs['arrival_time']:
            raise serializers.ValidationError("Arrival time must be after departure time.")
        return attrs


class TransportOptionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating transport options
    """
    class Meta:
        model = TransportOption
        fields = (
            'route_name', 'departure_location', 'destination', 'departure_time',
            'arrival_time', 'price', 'total_seats', 'days_of_operation'
        )
    
    def validate_days_of_operation(self, value):
        valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if not isinstance(value, list):
            raise serializers.ValidationError("Days of operation must be a list.")
        for day in value:
            if day not in valid_days:
                raise serializers.ValidationError(f"Invalid day: {day}. Must be one of {valid_days}")
        return value
    
    def validate(self, attrs):
        if attrs['departure_time'] >= attrs['arrival_time']:
            raise serializers.ValidationError("Arrival time must be after departure time.")
        return attrs


class TripUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for trip updates
    """
    organizer = TransportOrganizerSerializer(read_only=True)
    transport_option = TransportOptionSerializer(read_only=True)
    
    class Meta:
        model = TripUpdate
        fields = (
            'id', 'transport_option', 'organizer', 'update_type', 'title',
            'message', 'location_data', 'estimated_arrival', 'is_active', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class TripUpdateCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating trip updates
    """
    class Meta:
        model = TripUpdate
        fields = (
            'transport_option', 'update_type', 'title', 'message',
            'location_data', 'estimated_arrival'
        )
    
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


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for reviews
    """
    student = UserSerializer(read_only=True)
    transport_option = TransportOptionSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = (
            'id', 'booking', 'student', 'transport_option', 'rating',
            'comment', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating reviews
    """
    class Meta:
        model = Review
        fields = ('booking', 'transport_option', 'rating', 'comment')
    
    def validate_booking(self, value):
        # Check if booking belongs to the current user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if value.student.user != request.user:
                raise serializers.ValidationError("You can only review your own bookings.")
            if value.booking_status != 'completed':
                raise serializers.ValidationError("You can only review completed bookings.")
        return value
    
    def validate(self, attrs):
        # Check if review already exists for this booking
        if Review.objects.filter(booking=attrs['booking']).exists():
            raise serializers.ValidationError("Review already exists for this booking.")
        return attrs