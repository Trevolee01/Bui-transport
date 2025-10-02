"""
Serializers for User app
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, StudentProfile, TransportOrganizer


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 
            'phone_number', 'role', 'password', 'password_confirm'
        )
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password.')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details
    """
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 
            'phone_number', 'role', 'is_verified', 'date_joined'
        )
        read_only_fields = ('id', 'date_joined', 'is_verified')


class StudentProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for student profile
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = (
            'id', 'user', 'student_id', 'department', 'level', 
            'hostel_name', 'room_number', 'emergency_contact_name', 
            'emergency_contact_phone', 'is_verified', 'verification_date',
            'wallet_balance', 'created_at'
        )
        read_only_fields = ('id', 'is_verified', 'verification_date', 'wallet_balance', 'created_at')


class StudentProfileCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating student profile
    """
    class Meta:
        model = StudentProfile
        fields = (
            'student_id', 'department', 'level', 'hostel_name', 
            'room_number', 'emergency_contact_name', 'emergency_contact_phone'
        )


class TransportOrganizerSerializer(serializers.ModelSerializer):
    """
    Serializer for transport organizer profile
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = TransportOrganizer
        fields = (
            'id', 'user', 'business_name', 'license_number', 'vehicle_count',
            'bank_account_number', 'bank_name', 'account_holder_name',
            'mobile_money_number', 'approval_status', 'approval_date',
            'approved_by', 'rating', 'total_trips', 'total_earnings',
            'created_at'
        )
        read_only_fields = (
            'id', 'approval_status', 'approval_date', 'approved_by',
            'rating', 'total_trips', 'total_earnings', 'created_at'
        )


class TransportOrganizerCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating transport organizer profile
    """
    class Meta:
        model = TransportOrganizer
        fields = (
            'business_name', 'license_number', 'vehicle_count',
            'bank_account_number', 'bank_name', 'account_holder_name',
            'mobile_money_number'
        )


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value