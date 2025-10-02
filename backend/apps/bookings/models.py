"""
Booking models for BUI Transport System
"""
import uuid
from django.db import models
from datetime import date
from django.utils import timezone
from django.core.validators import MinValueValidator
from apps.users.models import User, StudentProfile
from apps.transport.models import TransportOption


class Booking(models.Model):
    """
    Student bookings for transport options
    """
    BOOKING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('wallet', 'Wallet'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
        ('card', 'Card'),
    ]
    
    REFUND_STATUS_CHOICES = [
        ('none', 'None'),
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processed', 'Processed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        StudentProfile, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    transport_option = models.ForeignKey(
        TransportOption, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    booking_date = models.DateField(default=date.today)
    seats_booked = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    organizer_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_reference = models.CharField(max_length=100, unique=True, blank=True, null=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    refund_status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='none')
    refund_reason = models.TextField(blank=True, null=True)
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bookings'
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.user.first_name} - {self.transport_option.route_name} ({self.booking_date})"
    
    def save(self, *args, **kwargs):
        # Calculate amounts if not set
        if not self.total_amount:
            self.total_amount = self.transport_option.price * self.seats_booked
        if not self.organizer_amount:
            # Platform fee is 5% of total amount
            self.platform_fee = self.total_amount * 0.05
            self.organizer_amount = self.total_amount - self.platform_fee
        
        super().save(*args, **kwargs)


class RefundRequest(models.Model):
    """
    Refund requests for bookings
    """
    REFUND_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processed', 'Processed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(
        Booking, 
        on_delete=models.CASCADE, 
        related_name='refund_requests'
    )
    student = models.ForeignKey(
        StudentProfile, 
        on_delete=models.CASCADE, 
        related_name='refund_requests'
    )
    organizer = models.ForeignKey(
        'users.TransportOrganizer', 
        on_delete=models.CASCADE, 
        related_name='refund_requests'
    )
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    processed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='processed_refunds'
    )
    processed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'refund_requests'
        verbose_name = 'Refund Request'
        verbose_name_plural = 'Refund Requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Refund Request - {self.booking} ({self.status})"