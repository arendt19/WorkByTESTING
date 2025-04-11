from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from jobs.models import Contract, Milestone
import uuid

class Transaction(models.Model):
    """
    Базовая модель для финансовых транзакций
    """
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('refunded', _('Refunded')),
    )
    
    TRANSACTION_TYPES = (
        ('deposit', _('Deposit')),          # Пополнение счета
        ('withdrawal', _('Withdrawal')),    # Вывод средств
        ('payment', _('Payment')),          # Оплата за работу
        ('refund', _('Refund')),           # Возврат средств
        ('fee', _('Service Fee')),         # Комиссия сервиса
    )
    
    transaction_id = models.CharField(_('Transaction ID'), max_length=50, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_type = models.CharField(_('Type'), max_length=20, choices=TRANSACTION_TYPES)
    description = models.TextField(_('Description'), blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    # Для связи с договором или вехой (опционально)
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    milestone = models.ForeignKey(Milestone, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    
    # Для связи с другими транзакциями (например, возврат средств ссылается на исходную транзакцию)
    related_transaction = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='related_transactions')
    
    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction_id} - {self.amount} ({self.get_transaction_type_display()})"
    
    def save(self, *args, **kwargs):
        # Генерируем уникальный ID транзакции
        if not self.transaction_id:
            uid = str(uuid.uuid4()).replace('-', '')[:10]
            self.transaction_id = f"TX-{uid}"
        super().save(*args, **kwargs)

class Wallet(models.Model):
    """
    Электронный кошелек пользователя
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    balance = models.DecimalField(_('Balance'), max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')
    
    def __str__(self):
        return f"Wallet of {self.user.username}"
    
    def deposit(self, amount, description="", related_transaction=None):
        """
        Метод для пополнения кошелька
        """
        if amount <= 0:
            raise ValueError(_("Amount must be positive"))
        
        # Создаем транзакцию
        transaction = Transaction.objects.create(
            user=self.user,
            amount=amount,
            transaction_type='deposit',
            status='completed',
            description=description,
            related_transaction=related_transaction
        )
        
        # Обновляем баланс
        self.balance += amount
        self.save()
        
        return transaction
    
    def withdraw(self, amount, description="", related_transaction=None):
        """
        Метод для вывода средств
        """
        if amount <= 0:
            raise ValueError(_("Amount must be positive"))
        
        if self.balance < amount:
            raise ValueError(_("Insufficient funds"))
        
        # Создаем транзакцию
        transaction = Transaction.objects.create(
            user=self.user,
            amount=amount,
            transaction_type='withdrawal',
            status='completed',
            description=description,
            related_transaction=related_transaction
        )
        
        # Обновляем баланс
        self.balance -= amount
        self.save()
        
        return transaction
    
    def payment(self, amount, contract, milestone=None, description=""):
        """
        Метод для выполнения оплаты по контракту/вехе
        """
        if amount <= 0:
            raise ValueError(_("Amount must be positive"))
        
        if self.balance < amount:
            raise ValueError(_("Insufficient funds"))
        
        # Создаем транзакцию
        transaction = Transaction.objects.create(
            user=self.user,
            amount=amount,
            transaction_type='payment',
            status='completed',
            description=description,
            contract=contract,
            milestone=milestone
        )
        
        # Расчет комиссии сервиса (например, 5%)
        service_fee = amount * 0.05
        
        # Обновляем баланс текущего пользователя (клиента)
        self.balance -= amount
        self.save()
        
        # Создаем транзакцию для комиссии сервиса
        Transaction.objects.create(
            user=self.user,
            amount=service_fee,
            transaction_type='fee',
            status='completed',
            description=_("Service fee for payment"),
            related_transaction=transaction
        )
        
        # Обновляем баланс фрилансера (за вычетом комиссии)
        freelancer_wallet, _ = Wallet.objects.get_or_create(user=contract.freelancer)
        freelancer_amount = amount - service_fee
        
        freelancer_transaction = Transaction.objects.create(
            user=contract.freelancer,
            amount=freelancer_amount,
            transaction_type='deposit',
            status='completed',
            description=_("Payment received for contract"),
            contract=contract,
            milestone=milestone,
            related_transaction=transaction
        )
        
        freelancer_wallet.balance += freelancer_amount
        freelancer_wallet.save()
        
        return transaction

class PaymentMethod(models.Model):
    """
    Сохраненный метод оплаты пользователя
    """
    METHOD_TYPES = (
        ('card', _('Credit/Debit Card')),
        ('bank', _('Bank Account')),
        ('paypal', _('PayPal')),
        ('crypto', _('Cryptocurrency')),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_methods'
    )
    method_type = models.CharField(_('Method Type'), max_length=20, choices=METHOD_TYPES)
    is_default = models.BooleanField(_('Default Method'), default=False)
    
    # Для карты
    card_last4 = models.CharField(_('Last 4 Digits'), max_length=4, blank=True)
    card_expiry = models.CharField(_('Expiry Date'), max_length=7, blank=True)  # формат MM/YYYY
    card_brand = models.CharField(_('Card Brand'), max_length=20, blank=True)
    
    # Для банковского счета
    bank_name = models.CharField(_('Bank Name'), max_length=100, blank=True)
    bank_account_last4 = models.CharField(_('Last 4 Digits'), max_length=4, blank=True)
    
    # Общие поля
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Payment Method')
        verbose_name_plural = _('Payment Methods')
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        if self.method_type == 'card':
            return f"{self.card_brand} **** {self.card_last4}"
        elif self.method_type == 'bank':
            return f"{self.bank_name} **** {self.bank_account_last4}"
        return self.get_method_type_display()
    
    def save(self, *args, **kwargs):
        # Если метод установлен как дефолтный, убираем дефолт у остальных методов данного пользователя
        if self.is_default:
            PaymentMethod.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
