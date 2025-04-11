from django import forms
from django.utils.translation import gettext_lazy as _
from .models import PaymentMethod
from decimal import Decimal

class DepositForm(forms.Form):
    """
    Форма для пополнения кошелька
    """
    AMOUNT_CHOICES = [
        (Decimal('100.00'), '100'),
        (Decimal('200.00'), '200'),
        (Decimal('500.00'), '500'),
        (Decimal('1000.00'), '1000'),
        (Decimal('2000.00'), '2000'),
    ]
    
    amount = forms.DecimalField(
        label=_('Amount'),
        min_value=Decimal('5.00'),
        max_value=Decimal('10000.00'),
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}),
        help_text=_('Enter the amount to deposit')
    )
    
    payment_method = forms.ModelChoiceField(
        label=_('Payment Method'),
        queryset=PaymentMethod.objects.none(),  # Будет перезаписано в __init__
        empty_label=None,
        help_text=_('Select a payment method or add a new one')
    )

class WithdrawForm(forms.Form):
    """
    Форма для вывода средств
    """
    amount = forms.DecimalField(
        label=_('Amount'),
        min_value=Decimal('10.00'),
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}),
        help_text=_('Enter the amount to withdraw')
    )
    
    payment_method = forms.ModelChoiceField(
        label=_('Payment Method'),
        queryset=PaymentMethod.objects.none(),  # Будет перезаписано в __init__
        empty_label=None,
        help_text=_('Select a payment method to receive funds')
    )
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < Decimal('10.00'):
            raise forms.ValidationError(_('Minimum withdrawal amount is $10.00'))
        return amount

class PaymentMethodForm(forms.ModelForm):
    """
    Форма для добавления/редактирования платежных методов
    """
    class Meta:
        model = PaymentMethod
        fields = [
            'method_type', 'is_default', 
            'card_last4', 'card_expiry', 'card_brand', 
            'bank_name', 'bank_account_last4'
        ]
        widgets = {
            'card_last4': forms.TextInput(attrs={'placeholder': '1234', 'maxlength': 4}),
            'card_expiry': forms.TextInput(attrs={'placeholder': 'MM/YYYY', 'maxlength': 7}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Добавляем класс формы в зависимости от типа метода
        self.fields['method_type'].widget.attrs.update({'class': 'method-type-select'})
        
        # Дополнительные классы для полей карты и банка
        for field_name in ['card_last4', 'card_expiry', 'card_brand']:
            self.fields[field_name].widget.attrs.update({'class': 'card-field'})
        
        for field_name in ['bank_name', 'bank_account_last4']:
            self.fields[field_name].widget.attrs.update({'class': 'bank-field'})
    
    def clean(self):
        cleaned_data = super().clean()
        method_type = cleaned_data.get('method_type')
        
        # Проверка полей для карты
        if method_type == 'card':
            card_last4 = cleaned_data.get('card_last4')
            card_expiry = cleaned_data.get('card_expiry')
            card_brand = cleaned_data.get('card_brand')
            
            if not card_last4:
                self.add_error('card_last4', _('This field is required for card payment method'))
            
            if not card_expiry:
                self.add_error('card_expiry', _('This field is required for card payment method'))
            
            if not card_brand:
                self.add_error('card_brand', _('This field is required for card payment method'))
        
        # Проверка полей для банка
        elif method_type == 'bank':
            bank_name = cleaned_data.get('bank_name')
            bank_account_last4 = cleaned_data.get('bank_account_last4')
            
            if not bank_name:
                self.add_error('bank_name', _('This field is required for bank payment method'))
            
            if not bank_account_last4:
                self.add_error('bank_account_last4', _('This field is required for bank payment method'))
        
        return cleaned_data 