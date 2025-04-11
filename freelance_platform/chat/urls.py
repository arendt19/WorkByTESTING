from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # Главная страница сообщений (входящие)
    path('', views.inbox_view, name='inbox'),
    
    # Просмотр и управление разговорами
    path('conversation/<int:pk>/', views.conversation_detail_view, name='conversation_detail'),
    path('start/<int:user_id>/', views.start_conversation_view, name='start_conversation'),
    
    # Уведомления
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:pk>/mark-read/', views.mark_notification_read_view, name='mark_notification_read'),
    path('api/mark-all-read/', views.mark_all_notifications_read_view, name='mark_all_notifications_read'),
    
    # API для получения количества непрочитанных сообщений/уведомлений
    path('api/unread/', views.api_unread_count_view, name='api_unread'),
] 