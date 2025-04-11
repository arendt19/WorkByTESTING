from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Управление кошельком
    path('wallet/', views.wallet_view, name='wallet'),
    path('transactions/', views.transaction_list_view, name='transaction_list'),
    path('transactions/<str:transaction_id>/', views.transaction_detail_view, name='transaction_detail'),
    
    # Пополнение и вывод средств
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    
    # Управление платежными методами
    path('payment-methods/', views.payment_methods_view, name='payment_methods'),
    path('payment-methods/add/', views.add_payment_method_view, name='add_payment_method'),
    path('payment-methods/<int:pk>/edit/', views.edit_payment_method_view, name='edit_payment_method'),
    path('payment-methods/<int:pk>/delete/', views.delete_payment_method_view, name='delete_payment_method'),
    
    # Оплата вех
    path('pay-milestone/<int:milestone_id>/', views.pay_milestone_view, name='pay_milestone'),
] 