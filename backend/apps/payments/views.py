"""
Views for Payments app
"""
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Q
from django.utils import timezone
import uuid

from .models import PaymentMethod, Transaction, WalletTransaction, AuditLog
from .serializers import (
    PaymentMethodSerializer, PaymentMethodCreateSerializer,
    TransactionSerializer, TransactionCreateSerializer,
    WalletTransactionSerializer, WalletTopupSerializer,
    AuditLogSerializer
)


class PaymentMethodListView(generics.ListCreateAPIView):
    """
    List and create payment methods
    """
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['-is_primary', 'created_at']
    
    def get_queryset(self):
        try:
            student_profile = self.request.user.student_profile
            return PaymentMethod.objects.filter(
                student=student_profile,
                is_active=True
            )
        except AttributeError:
            return PaymentMethod.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaymentMethodCreateSerializer
        return PaymentMethodSerializer
    
    def perform_create(self, serializer):
        try:
            student_profile = self.request.user.student_profile
            serializer.save(student=student_profile)
        except AttributeError:
            raise PermissionError("Student profile not found.")


class PaymentMethodDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a payment method
    """
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        try:
            student_profile = self.request.user.student_profile
            return PaymentMethod.objects.filter(student=student_profile)
        except AttributeError:
            return PaymentMethod.objects.none()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PaymentMethodCreateSerializer
        return PaymentMethodSerializer


class TransactionListView(generics.ListAPIView):
    """
    List transactions for the current user
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.role == 'student':
            try:
                student_profile = self.request.user.student_profile
                return Transaction.objects.filter(student=student_profile)
            except AttributeError:
                return Transaction.objects.none()
        elif self.request.user.role == 'transport_organizer':
            try:
                organizer = self.request.user.organizer_profile
                return Transaction.objects.filter(organizer=organizer)
            except AttributeError:
                return Transaction.objects.none()
        elif self.request.user.role == 'admin':
            return Transaction.objects.all()
        else:
            return Transaction.objects.none()


class TransactionDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific transaction
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'student':
            try:
                student_profile = self.request.user.student_profile
                return Transaction.objects.filter(student=student_profile)
            except AttributeError:
                return Transaction.objects.none()
        elif self.request.user.role == 'transport_organizer':
            try:
                organizer = self.request.user.organizer_profile
                return Transaction.objects.filter(organizer=organizer)
            except AttributeError:
                return Transaction.objects.none()
        elif self.request.user.role == 'admin':
            return Transaction.objects.all()
        else:
            return Transaction.objects.none()


class WalletTransactionListView(generics.ListAPIView):
    """
    List wallet transactions for the current user
    """
    serializer_class = WalletTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        try:
            student_profile = self.request.user.student_profile
            return WalletTransaction.objects.filter(student=student_profile)
        except AttributeError:
            return WalletTransaction.objects.none()


class WalletTopupView(generics.CreateAPIView):
    """
    Top up wallet
    """
    serializer_class = WalletTopupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Ensure only students can top up wallet
        if self.request.user.role != 'student':
            raise PermissionError("Only students can top up wallet.")
        
        try:
            student_profile = self.request.user.student_profile
            amount = serializer.validated_data['amount']
            payment_method_id = serializer.validated_data['payment_method_id']
            
            # Get payment method
            payment_method = PaymentMethod.objects.get(
                id=payment_method_id,
                student=student_profile,
                is_active=True
            )
            
            # Create transaction
            transaction = Transaction.objects.create(
                student=student_profile,
                transaction_type='wallet_topup',
                amount=amount,
                payment_method=payment_method.method_type,
                payment_reference=str(uuid.uuid4()),
                description=f"Wallet top-up via {payment_method.provider_name}",
                status='pending'
            )
            
            # Create wallet transaction
            balance_before = student_profile.wallet_balance
            balance_after = balance_before + amount
            
            WalletTransaction.objects.create(
                student=student_profile,
                transaction_type='credit',
                amount=amount,
                balance_before=balance_before,
                balance_after=balance_after,
                reference_type='topup',
                reference_id=transaction.id,
                description=f"Wallet top-up via {payment_method.provider_name}"
            )
            
            # Update wallet balance
            student_profile.wallet_balance = balance_after
            student_profile.save()
            
            # Update transaction status
            transaction.status = 'success'
            transaction.processed_at = timezone.now()
            transaction.save()
            
        except AttributeError:
            raise PermissionError("Student profile not found.")
        except PaymentMethod.DoesNotExist:
            raise PermissionError("Invalid payment method.")


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def wallet_balance(request):
    """
    Get current wallet balance
    """
    try:
        student_profile = request.user.student_profile
        return Response({
            'balance': student_profile.wallet_balance,
            'currency': 'NGN'
        })
    except AttributeError:
        return Response(
            {'error': 'Student profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def payment_stats(request):
    """
    Get payment statistics for the current user
    """
    try:
        if request.user.role == 'student':
            student_profile = request.user.student_profile
            
            # Get transaction statistics
            transactions = Transaction.objects.filter(student=student_profile)
            
            stats = {
                'total_transactions': transactions.count(),
                'successful_transactions': transactions.filter(status='success').count(),
                'failed_transactions': transactions.filter(status='failed').count(),
                'total_amount_spent': transactions.filter(
                    status='success',
                    transaction_type='payment'
                ).aggregate(total=Sum('amount'))['total'] or 0,
                'total_topups': transactions.filter(
                    status='success',
                    transaction_type='wallet_topup'
                ).aggregate(total=Sum('amount'))['total'] or 0,
                'wallet_balance': student_profile.wallet_balance,
            }
            
        elif request.user.role == 'transport_organizer':
            organizer = request.user.organizer_profile
            
            # Get transaction statistics
            transactions = Transaction.objects.filter(organizer=organizer)
            
            stats = {
                'total_transactions': transactions.count(),
                'successful_transactions': transactions.filter(status='success').count(),
                'failed_transactions': transactions.filter(status='failed').count(),
                'total_earnings': transactions.filter(
                    status='success',
                    transaction_type='payout'
                ).aggregate(total=Sum('amount'))['total'] or 0,
                'pending_payouts': transactions.filter(
                    status='pending',
                    transaction_type='payout'
                ).aggregate(total=Sum('amount'))['total'] or 0,
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


class AuditLogListView(generics.ListAPIView):
    """
    List audit logs (admin only)
    """
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return AuditLog.objects.all()
        else:
            return AuditLog.objects.none()