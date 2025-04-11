from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.db import transaction as db_transaction
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.db import models
from django.utils import timezone

from .models import Wallet, Transaction, PaymentMethod
from .forms import DepositForm, WithdrawForm, PaymentMethodForm
from jobs.models import Contract, Milestone

@login_required
def wallet_view(request):
    """
    Отображение кошелька пользователя и краткой статистики транзакций
    """
    user = request.user
    wallet, created = Wallet.objects.get_or_create(user=user)
    
    # Получаем транзакции пользователя
    transactions = Transaction.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Статистика транзакций
    stats = {
        'income': Transaction.objects.filter(
            user=user, 
            transaction_type__in=['deposit', 'payment'],
            status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or 0,
        
        'expense': Transaction.objects.filter(
            user=user, 
            transaction_type__in=['withdrawal', 'fee'],
            status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or 0,
        
        'pending': Transaction.objects.filter(
            user=user, 
            status='pending'
        ).aggregate(total=models.Sum('amount'))['total'] or 0
    }
    
    # Статистика по месяцам (для графика)
    current_year = timezone.now().year
    monthly_stats = []
    
    for month in range(1, 13):
        month_income = Transaction.objects.filter(
            user=user,
            transaction_type__in=['deposit', 'payment'],
            status='completed',
            created_at__year=current_year,
            created_at__month=month
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        month_expense = Transaction.objects.filter(
            user=user,
            transaction_type__in=['withdrawal', 'fee'],
            status='completed',
            created_at__year=current_year,
            created_at__month=month
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        monthly_stats.append({
            'month': month,
            'month_name': timezone.datetime(current_year, month, 1).strftime('%b'),
            'income': month_income,
            'expense': month_expense,
            'balance': month_income - month_expense
        })
    
    # Статистика по категориям транзакций
    transaction_types = {
        'deposit': _('Deposits'),
        'withdrawal': _('Withdrawals'),
        'payment': _('Payments'),
        'refund': _('Refunds'),
        'fee': _('Service Fees'),
    }
    
    type_stats = []
    for t_type, label in transaction_types.items():
        amount = Transaction.objects.filter(
            user=user,
            transaction_type=t_type,
            status='completed'
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        type_stats.append({
            'type': t_type,
            'label': label,
            'amount': amount,
        })
    
    # Информация о платежных методах пользователя
    payment_methods = PaymentMethod.objects.filter(user=user, is_active=True)
    
    context = {
        'wallet': wallet,
        'transactions': transactions,
        'stats': stats,
        'monthly_stats': monthly_stats,
        'type_stats': type_stats,
        'payment_methods': payment_methods,
    }
    
    return render(request, 'payments/wallet.html', context)

@login_required
def transaction_list_view(request):
    """
    Отображает список всех транзакций пользователя
    """
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    
    # Фильтрация по типу
    transaction_type = request.GET.get('type')
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    
    context = {
        'transactions': transactions,
    }
    
    return render(request, 'payments/transaction_list.html', context)

@login_required
def transaction_detail_view(request, transaction_id):
    """
    Отображает детальную информацию о транзакции
    """
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id, user=request.user)
    
    context = {
        'transaction': transaction,
    }
    
    return render(request, 'payments/transaction_detail.html', context)

@login_required
def deposit_view(request):
    """
    Страница для пополнения кошелька
    """
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    
    # Получаем платежные методы пользователя
    payment_methods = PaymentMethod.objects.filter(user=request.user, is_active=True)
    
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_method_id = form.cleaned_data['payment_method']
            
            try:
                payment_method = PaymentMethod.objects.get(pk=payment_method_id, user=request.user)
                
                # В реальном приложении здесь был бы код для обработки платежа через платежный шлюз
                # Для демо просто создаем транзакцию и пополняем кошелек
                
                with db_transaction.atomic():
                    description = _("Deposit via {method}").format(method=payment_method)
                    wallet.deposit(amount, description=description)
                
                messages.success(request, _("Your wallet has been successfully funded with {amount}").format(amount=amount))
                return redirect('payments:wallet')
                
            except PaymentMethod.DoesNotExist:
                messages.error(request, _("Invalid payment method"))
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = DepositForm()
        form.fields['payment_method'].queryset = payment_methods
    
    context = {
        'wallet': wallet,
        'form': form,
        'payment_methods': payment_methods,
    }
    
    return render(request, 'payments/deposit.html', context)

@login_required
def withdraw_view(request):
    """
    Страница для вывода средств
    """
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    
    # Получаем платежные методы пользователя
    payment_methods = PaymentMethod.objects.filter(user=request.user, is_active=True)
    
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_method_id = form.cleaned_data['payment_method']
            
            try:
                payment_method = PaymentMethod.objects.get(pk=payment_method_id, user=request.user)
                
                # Проверка баланса и вывод средств
                
                with db_transaction.atomic():
                    description = _("Withdrawal to {method}").format(method=payment_method)
                    wallet.withdraw(amount, description=description)
                
                messages.success(request, _("Withdrawal request for {amount} has been processed").format(amount=amount))
                return redirect('payments:wallet')
                
            except PaymentMethod.DoesNotExist:
                messages.error(request, _("Invalid payment method"))
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = WithdrawForm()
        form.fields['payment_method'].queryset = payment_methods
    
    context = {
        'wallet': wallet,
        'form': form,
        'payment_methods': payment_methods,
    }
    
    return render(request, 'payments/withdraw.html', context)

@login_required
def payment_methods_view(request):
    """
    Страница для управления платежными методами
    """
    payment_methods = PaymentMethod.objects.filter(user=request.user)
    
    context = {
        'payment_methods': payment_methods,
    }
    
    return render(request, 'payments/payment_methods.html', context)

@login_required
def add_payment_method_view(request):
    """
    Страница для добавления нового платежного метода
    """
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.user = request.user
            payment_method.save()
            
            messages.success(request, _("Payment method added successfully"))
            return redirect('payments:payment_methods')
    else:
        form = PaymentMethodForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'payments/add_payment_method.html', context)

@login_required
def edit_payment_method_view(request, pk):
    """
    Страница для редактирования платежного метода
    """
    payment_method = get_object_or_404(PaymentMethod, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST, instance=payment_method)
        if form.is_valid():
            form.save()
            
            messages.success(request, _("Payment method updated successfully"))
            return redirect('payments:payment_methods')
    else:
        form = PaymentMethodForm(instance=payment_method)
    
    context = {
        'form': form,
        'payment_method': payment_method,
    }
    
    return render(request, 'payments/edit_payment_method.html', context)

@login_required
def delete_payment_method_view(request, pk):
    """
    Удаление платежного метода
    """
    payment_method = get_object_or_404(PaymentMethod, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Если это дефолтный метод оплаты, находим другой
        if payment_method.is_default:
            other_method = PaymentMethod.objects.filter(user=request.user).exclude(pk=pk).first()
            if other_method:
                other_method.is_default = True
                other_method.save()
        
        payment_method.delete()
        messages.success(request, _("Payment method deleted successfully"))
        return redirect('payments:payment_methods')
    
    context = {
        'payment_method': payment_method,
    }
    
    return render(request, 'payments/delete_payment_method.html', context)

@login_required
def pay_milestone_view(request, milestone_id):
    """
    Оплата вехи проекта
    """
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    contract = milestone.contract
    
    # Проверяем, что пользователь является клиентом контракта
    if contract.client != request.user:
        return HttpResponseForbidden(_("You don't have permission to pay for this milestone"))
    
    # Проверяем, что веха находится в статусе "approved"
    if milestone.status != 'approved':
        messages.error(request, _("This milestone is not approved for payment"))
        return redirect('jobs:contract_detail', pk=contract.pk)
    
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    
    # Проверяем достаточно ли средств
    if wallet.balance < milestone.amount:
        messages.error(request, _("Insufficient funds in your wallet"))
        return redirect('payments:deposit')
    
    if request.method == 'POST':
        try:
            with db_transaction.atomic():
                description = _("Payment for milestone '{title}'").format(title=milestone.title)
                wallet.payment(milestone.amount, contract, milestone, description)
                
                # Обновляем статус вехи
                milestone.status = 'paid'
                milestone.save()
                
                # Проверяем, все ли вехи оплачены
                all_milestones_paid = all(
                    m.status == 'paid' for m in contract.milestones.all()
                )
                
                # Если все вехи оплачены, завершаем контракт
                if all_milestones_paid:
                    contract.status = 'completed'
                    contract.save()
            
            messages.success(request, _("Payment for milestone completed successfully"))
            return redirect('jobs:contract_detail', pk=contract.pk)
            
        except ValueError as e:
            messages.error(request, str(e))
    
    context = {
        'milestone': milestone,
        'contract': contract,
        'wallet': wallet,
    }
    
    return render(request, 'payments/pay_milestone.html', context)
