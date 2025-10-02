"""
Serializers for Payments app
"""
from rest_framework import serializers
from .models import PaymentMethod, Transaction, WalletTransaction, AuditLog
from apps.users.serializers import StudentProfileSerializer
from apps.bookings.serializers import BookingSerializer


class PaymentMethodSerializer(serializers.ModelSerializer):
    """
    Serializer for payment methods
    """
    student = StudentProfileSerializer(read_only=True)
    
    class Meta:
        model = PaymentMethod
        fields = (
            'id', 'student', 'method_type', 'provider_name', 'account_number',
            'account_name', 'is_primary', 'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_account_number(self, value):
        # Basic validation for different payment method types
        method_type = self.initial_data.get('method_type')
        
        if method_type == 'mobile_money':
            # Validate phone number format
            if not value.startswith('+') and not value.startswith('0'):
                raise serializers.ValidationError("Mobile money number must start with + or 0")
        elif method_type == 'bank_card':
            # Validate card number (basic check)
            if not value.replace(' ', '').replace('-', '').isdigit():
                raise serializers.ValidationError("Card number must contain only digits")
        elif method_type == 'bank_account':
            # Validate account number (basic check)
            if not value.isdigit():
                raise serializers.ValidationError("Account number must contain only digits")
        
        return value


class PaymentMethodCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating payment methods
    """
    class Meta:
        model = PaymentMethod
        fields = (
            'method_type', 'provider_name', 'account_number', 'account_name', 'is_primary'
        )
    
    def validate_account_number(self, value):
        # Basic validation for different payment method types
        method_type = self.initial_data.get('method_type')
        
        if method_type == 'mobile_money':
            # Validate phone number format
            if not value.startswith('+') and not value.startswith('0'):
                raise serializers.ValidationError("Mobile money number must start with + or 0")
        elif method_type == 'bank_card':
            # Validate card number (basic check)
            if not value.replace(' ', '').replace('-', '').isdigit():
                raise serializers.ValidationError("Card number must contain only digits")
        elif method_type == 'bank_account':
            # Validate account number (basic check)
            if not value.isdigit():
                raise serializers.ValidationError("Account number must contain only digits")
        
        return value
    
    def validate(self, attrs):
        # Ensure only one primary payment method per student
        if attrs.get('is_primary'):
            request = self.context.get('request')
            if request and hasattr(request, 'user'):
                try:
                    student_profile = request.user.student_profile
                    if PaymentMethod.objects.filter(
                        student=student_profile, 
                        is_primary=True, 
                        is_active=True
                    ).exists():
                        raise serializers.ValidationError("Only one primary payment method is allowed.")
                except AttributeError:
                    raise serializers.ValidationError("Student profile not found.")
        
        return attrs


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for transactions
    """
    student = StudentProfileSerializer(read_only=True)
    booking = BookingSerializer(read_only=True)
    
    class Meta:
        model = Transaction
        fields = (
            'id', 'booking', 'student', 'organizer', 'transaction_type', 'amount',
            'currency', 'payment_method', 'payment_reference', 'external_reference',
            'status', 'gateway_response', 'description', 'processed_at', 'created_at'
        )
        read_only_fields = (
            'id', 'payment_reference', 'external_reference', 'gateway_response',
            'processed_at', 'created_at'
        )


class TransactionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating transactions
    """
    class Meta:
        model = Transaction
        fields = (
            'booking', 'transaction_type', 'amount', 'currency', 'payment_method',
            'description'
        )
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value


class WalletTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for wallet transactions
    """
    student = StudentProfileSerializer(read_only=True)
    
    class Meta:
        model = WalletTransaction
        fields = (
            'id', 'student', 'transaction_type', 'amount', 'balance_before',
            'balance_after', 'reference_type', 'reference_id', 'description', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class WalletTopupSerializer(serializers.Serializer):
    """
    Serializer for wallet top-up
    """
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.ChoiceField(choices=PaymentMethod.METHOD_TYPE_CHOICES)
    payment_method_id = serializers.UUIDField()
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        if value < 100:  # Minimum top-up amount
            raise serializers.ValidationError("Minimum top-up amount is ₦100.")
        return value
    
    def validate_payment_method_id(self, value):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            try:
                student_profile = request.user.student_profile
                payment_method = PaymentMethod.objects.get(
                    id=value,
                    student=student_profile,
                    is_active=True
                )
                return value
            except PaymentMethod.DoesNotExist:
                raise serializers.ValidationError("Invalid payment method.")
        return value


class AuditLogSerializer(serializers.ModelSerializer):
    """
    Serializer for audit logs
    """
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = AuditLog
        fields = (
            'id', 'user', 'action', 'table_name', 'record_id', 'old_values',
            'new_values', 'ip_address', 'user_agent', 'created_at'
        )
        read_only_fields = ('id', 'created_at')