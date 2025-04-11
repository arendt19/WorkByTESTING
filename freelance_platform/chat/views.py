from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Conversation, Message, Notification
from .forms import MessageForm

User = get_user_model()

@login_required
def inbox_view(request):
    """
    Показывает список всех разговоров пользователя
    """
    # Получаем все разговоры, в которых участвует текущий пользователь
    conversations = Conversation.objects.filter(participants=request.user)
    
    # Подсчитываем количество непрочитанных сообщений для каждого разговора
    for conversation in conversations:
        conversation.unread_count = Message.objects.filter(
            conversation=conversation, 
            is_read=False
        ).exclude(sender=request.user).count()
    
    context = {
        'conversations': conversations,
    }
    
    return render(request, 'chat/inbox.html', context)

@login_required
def conversation_detail_view(request, pk):
    """
    Отображает конкретный разговор и форму для отправки новых сообщений
    """
    conversation = get_object_or_404(
        Conversation.objects.filter(participants=request.user),
        pk=pk
    )
    
    # Получаем все сообщения для данного разговора
    messages = conversation.messages.all()
    
    # Отмечаем непрочитанные сообщения как прочитанные
    for message in messages:
        if message.sender != request.user and not message.is_read:
            message.mark_as_read()
    
    # Создаем форму для нового сообщения
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            
            # Создаем уведомление для получателя
            Notification.create_message_notification(message)
            
            # Обновляем время последнего обновления разговора
            conversation.save()  # Это автоматически обновит updated_at
            
            return redirect('chat:conversation_detail', pk=conversation.pk)
    else:
        form = MessageForm()
    
    # Получаем другого участника разговора (не текущего пользователя)
    other_participant = conversation.participants.exclude(id=request.user.id).first()
    
    context = {
        'conversation': conversation,
        'messages': messages,
        'form': form,
        'other_participant': other_participant,
    }
    
    return render(request, 'chat/conversation_detail.html', context)

@login_required
def start_conversation_view(request, user_id):
    """
    Начинает новый разговор с пользователем или открывает существующий
    """
    # Получаем пользователя, с которым хотим начать разговор
    other_user = get_object_or_404(User, pk=user_id)
    
    # Нельзя начать разговор с самим собой
    if other_user == request.user:
        return redirect('chat:inbox')
    
    # Получаем или создаем разговор между этими пользователями
    conversation = Conversation.get_or_create_conversation(request.user, other_user)
    
    return redirect('chat:conversation_detail', pk=conversation.pk)

@login_required
def notifications_view(request):
    """
    Отображает все уведомления пользователя
    """
    notifications = Notification.objects.filter(user=request.user)
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, 'chat/notifications.html', context)

@login_required
def mark_notification_read_view(request, pk):
    """
    Отмечает уведомление как прочитанное и перенаправляет на связанный объект
    """
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_as_read()
    
    # Перенаправляем на связанный объект в зависимости от типа уведомления
    if notification.notification_type == 'message' and notification.related_object_id:
        return redirect('chat:conversation_detail', pk=notification.related_object_id)
    elif notification.notification_type == 'proposal' and notification.related_object_id:
        return redirect('jobs:proposal_detail', pk=notification.related_object_id)
    elif notification.notification_type == 'contract' and notification.related_object_id:
        return redirect('jobs:contract_detail', pk=notification.related_object_id)
    elif notification.notification_type == 'milestone' and notification.related_object_id:
        # Перенаправляем на контракт, содержащий вехи
        from jobs.models import Milestone
        milestone = get_object_or_404(Milestone, pk=notification.related_object_id)
        return redirect('jobs:contract_detail', pk=milestone.contract.pk)
    elif notification.notification_type == 'review' and notification.related_object_id:
        # Перенаправляем на профиль фрилансера
        from accounts.models import User
        freelancer = get_object_or_404(User, pk=notification.related_object_id)
        return redirect('freelancer_detail', username=freelancer.username)
    
    # Если не удалось определить, куда перенаправить
    return redirect('chat:notifications')

@login_required
def api_unread_count_view(request):
    """
    API для получения количества непрочитанных сообщений и уведомлений
    """
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        unread_messages = Message.objects.filter(
            conversation__participants=request.user,
            is_read=False
        ).exclude(sender=request.user).count()
        
        unread_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        data = {
            'unread_messages': unread_messages,
            'unread_notifications': unread_notifications,
            'total_unread': unread_messages + unread_notifications,
        }
        
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def mark_all_notifications_read_view(request):
    """
    Отмечает все уведомления пользователя как прочитанные
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Отмечаем все уведомления как прочитанные
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
