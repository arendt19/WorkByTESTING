from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Главная и общие страницы
    path('', views.home_view, name='home'),
    path('projects/', views.project_list_view, name='project_list'),
    path('projects/<int:pk>/', views.project_detail_view, name='project_detail'),
    
    # Управление проектами для клиентов
    path('projects/create/', views.project_create_view, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_edit_view, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete_view, name='project_delete'),
    path('my-projects/', views.my_projects_view, name='my_projects'),
    
    # Управление предложениями для фрилансеров
    path('projects/<int:project_pk>/propose/', views.proposal_create_view, name='proposal_create'),
    path('proposals/<int:pk>/edit/', views.proposal_edit_view, name='proposal_edit'),
    path('proposals/<int:pk>/withdraw/', views.proposal_withdraw_view, name='proposal_withdraw'),
    path('proposals/<int:pk>/', views.proposal_detail_view, name='proposal_detail'),
    path('my-proposals/', views.my_proposals_view, name='my_proposals'),
    
    # Принятие предложений и создание контрактов
    path('proposals/<int:pk>/accept/', views.proposal_accept_view, name='proposal_accept'),
    path('contracts/create/', views.contract_create_view, name='contract_create'),
    path('contracts/<int:pk>/', views.contract_detail_view, name='contract_detail'),
    path('contracts/', views.contract_list_view, name='contract_list'),
    
    # Управление вехами
    path('milestones/<int:pk>/submit/', views.milestone_submit_view, name='milestone_submit'),
    path('milestones/<int:pk>/approve/', views.milestone_approve_view, name='milestone_approve'),
    path('milestones/<int:pk>/reject/', views.milestone_reject_view, name='milestone_reject'),
    
    # Категории
    path('categories/', views.category_list_view, name='category_list'),
    path('categories/<slug:slug>/', views.category_detail_view, name='category_detail'),
    
    # Фрилансеры
    path('freelancers/', views.freelancer_list_view, name='freelancer_list'),
] 