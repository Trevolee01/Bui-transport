"""
User models for BUI Transport System
"""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom User model with role-based authentication
    """
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('transport_organizer', 'Transport Organizer'),
        ('admin', 'Administrator'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=11,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{0,11}$',
            message="Phone number must be entered. Up to 11 digits allowed."
        )]
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class StudentProfile(models.Model):
    """
    Extended profile for students
    """
    LEVEL_CHOICES = [
        (100, '100 Level'),
        (200, '200 Level'),
        (300, '300 Level'),
        (400, '400 Level'),
        (500, '500 Level'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True, help_text="University Student ID")
    department = models.CharField(max_length=100)
    level = models.IntegerField(choices=LEVEL_CHOICES)
    hostel_name = models.CharField(max_length=100, blank=True, null=True)
    room_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(
        max_length=11,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{0,11}$',
            message="Phone number must be entered. Up to 11 digits allowed."
        )]
    )
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(blank=True, null=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_profiles'
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.student_id}"


class TransportOrganizer(models.Model):
    """
    Profile for transport organizers
    """
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organizer_profile')
    business_name = models.CharField(max_length=200)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    vehicle_count = models.IntegerField(default=0)
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_holder_name = models.CharField(max_length=200, blank=True, null=True)
    mobile_money_number = models.CharField(max_length=20, blank=True, null=True)
    approval_status = models.CharField(
        max_length=20, 
        choices=APPROVAL_STATUS_CHOICES, 
        default='pending'
    )
    approval_date = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_organizers'
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_trips = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'transport_organizers'
        verbose_name = 'Transport Organizer'
        verbose_name_plural = 'Transport Organizers'
    
    def __str__(self):
        return f"{self.business_name} - {self.user.email}"