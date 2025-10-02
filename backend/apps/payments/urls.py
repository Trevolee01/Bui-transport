"""
URLs for Payments app
"""
from django.urls import path
from . import views

urlpatterns = [
    # Payment method endpoints
    path('methods/', views.PaymentMethodListView.as_view(), name='payment-methods-list'),
    path('methods/<uuid:pk>/', views.PaymentMethodDetailView.as_view(), name='payment-method-detail'),
    
    # Transaction endpoints
    path('transactions/', views.TransactionListView.as_view(), name='transactions-list'),
    path('transactions/<uuid:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    
    # Wallet endpoints
    path('wallet/transactions/', views.WalletTransactionListView.as_view(), name='wallet-transactions-list'),
    path('wallet/topup/', views.WalletTopupView.as_view(), name='wallet-topup'),
    path('wallet/balance/', views.wallet_balance, name='wallet-balance'),
    
    # Statistics endpoints
    path('stats/', views.payment_stats, name='payment-stats'),
    
    # Audit log endpoints (admin only)
    path('audit-logs/', views.AuditLogListView.as_view(), name='audit-logs-list'),
]