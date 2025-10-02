"""
Transport models for BUI Transport System
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.users.models import User, TransportOrganizer


class TransportOption(models.Model):
    """
    Transport options/routes offered by organizers
    """
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer = models.ForeignKey(
        TransportOrganizer, 
        on_delete=models.CASCADE, 
        related_name='transport_options'
    )
    route_name = models.CharField(max_length=200)
    departure_location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_seats = models.IntegerField(validators=[MinValueValidator(1)])
    available_seats = models.IntegerField(validators=[MinValueValidator(0)])
    days_of_operation = models.JSONField(default=list, help_text="List of days: ['monday', 'tuesday', ...]")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'transport_options'
        verbose_name = 'Transport Option'
        verbose_name_plural = 'Transport Options'
        ordering = ['departure_time']
    
    def __str__(self):
        return f"{self.route_name} - {self.departure_location} to {self.destination}"
    
    def save(self, *args, **kwargs):
        # Ensure available_seats doesn't exceed total_seats
        if self.available_seats > self.total_seats:
            self.available_seats = self.total_seats
        super().save(*args, **kwargs)


class TripUpdate(models.Model):
    """
    Real-time updates for transport options
    """
    UPDATE_TYPE_CHOICES = [
        ('delay', 'Delay'),
        ('cancellation', 'Cancellation'),
        ('route_change', 'Route Change'),
        ('location', 'Location Update'),
        ('general', 'General Update'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transport_option = models.ForeignKey(
        TransportOption, 
        on_delete=models.CASCADE, 
        related_name='trip_updates'
    )
    organizer = models.ForeignKey(
        TransportOrganizer, 
        on_delete=models.CASCADE, 
        related_name='trip_updates'
    )
    update_type = models.CharField(max_length=20, choices=UPDATE_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    location_data = models.JSONField(
        blank=True, 
        null=True, 
        help_text="GPS coordinates: {'lat': 6.5244, 'lng': 3.3792}"
    )
    estimated_arrival = models.TimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'trip_updates'
        verbose_name = 'Trip Update'
        verbose_name_plural = 'Trip Updates'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transport_option.route_name} - {self.title}"


class Review(models.Model):
    """
    Reviews for transport options
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking_id = models.UUIDField(help_text="ID of the booking this review is for")
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    transport_option = models.ForeignKey(
        TransportOption, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5"
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reviews'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        unique_together = ['booking_id', 'student', 'transport_option']
    
    def __str__(self):
        return f"{self.student.first_name} - {self.transport_option.route_name} ({self.rating}/5)"