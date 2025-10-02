"""
Payment models for BUI Transport System
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from apps.users.models import User, StudentProfile
from apps.bookings.models import Booking


class PaymentMethod(models.Model):
    """
    Payment methods for students
    """
    METHOD_TYPE_CHOICES = [
        ('mobile_money', 'Mobile Money'),
        ('bank_card', 'Bank Card'),
        ('bank_account', 'Bank Account'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        StudentProfile, 
        on_delete=models.CASCADE, 
        related_name='payment_methods'
    )
    method_type = models.CharField(max_length=20, choices=METHOD_TYPE_CHOICES)
    provider_name = models.CharField(max_length=100, help_text="MTN, Airtel, Visa, MasterCard, etc.")
    account_number = models.CharField(max_length=100, help_text="Phone number, card number, or account number")
    account_name = models.CharField(max_length=200)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment_methods'
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Methods'
        ordering = ['-is_primary', 'created_at']
    
    def __str__(self):
        return f"{self.student.user.first_name} - {self.get_method_type_display()} ({self.provider_name})"


class Transaction(models.Model):
    """
    Financial transactions
    """
    TRANSACTION_TYPE_CHOICES = [
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('wallet_topup', 'Wallet Top-up'),
        ('payout', 'Payout'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('wallet', 'Wallet'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
        ('card', 'Card'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(
        Booking, 
        on_delete=models.CASCADE, 
        related_name='transactions',
        blank=True,
        null=True
    )
    student = models.ForeignKey(
        StudentProfile, 
        on_delete=models.CASCADE, 
        related_name='transactions'
    )
    organizer = models.ForeignKey(
        'users.TransportOrganizer', 
        on_delete=models.CASCADE, 
        related_name='transactions',
        blank=True,
        null=True
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='NGN')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_reference = models.CharField(max_length=100, unique=True)
    external_reference = models.CharField(max_length=100, blank=True, null=True, help_text="Payment gateway reference")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    gateway_response = models.JSONField(blank=True, null=True, help_text="Response from payment gateway")
    description = models.TextField(blank=True, null=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} {self.currency} ({self.status})"


class WalletTransaction(models.Model):
    """
    Wallet transactions for students
    """
    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]
    
    REFERENCE_TYPE_CHOICES = [
        ('booking', 'Booking'),
        ('refund', 'Refund'),
        ('topup', 'Top-up'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        StudentProfile, 
        on_delete=models.CASCADE, 
        related_name='wallet_transactions'
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    balance_before = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    reference_type = models.CharField(max_length=20, choices=REFERENCE_TYPE_CHOICES)
    reference_id = models.UUIDField(blank=True, null=True, help_text="ID of related booking or transaction")
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'wallet_transactions'
        verbose_name = 'Wallet Transaction'
        verbose_name_plural = 'Wallet Transactions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.user.first_name} - {self.get_transaction_type_display()} {self.amount}"


class AuditLog(models.Model):
    """
    Audit logs for tracking system changes
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=100)
    table_name = models.CharField(max_length=100, blank=True, null=True)
    record_id = models.UUIDField(blank=True, null=True)
    old_values = models.JSONField(blank=True, null=True)
    new_values = models.JSONField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_logs'
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.action} - {self.table_name} ({self.created_at})"