from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
import uuid

class Category(models.Model):
    """
    Категории проектов
    """
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('jobs:category_detail', args=[self.slug])

class Tag(models.Model):
    """
    Теги для проектов
    """
    name = models.CharField(_('Name'), max_length=50, unique=True)
    slug = models.SlugField(_('Slug'), max_length=50, unique=True)
    
    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Project(models.Model):
    """
    Проектная работа, размещаемая клиентами
    """
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('open', _('Open')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    )
    
    BUDGET_TYPE_CHOICES = (
        ('fixed', _('Fixed Price')),
        ('hourly', _('Hourly Rate')),
    )
    
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='client_projects'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='projects'
    )
    tags = models.ManyToManyField(
        Tag, 
        blank=True, 
        related_name='projects'
    )
    budget_type = models.CharField(
        _('Budget Type'), 
        max_length=10, 
        choices=BUDGET_TYPE_CHOICES
    )
    budget_min = models.DecimalField(
        _('Minimum Budget'), 
        max_digits=10, 
        decimal_places=2
    )
    budget_max = models.DecimalField(
        _('Maximum Budget'), 
        max_digits=10, 
        decimal_places=2
    )
    deadline = models.DateTimeField(_('Deadline'), null=True, blank=True)
    status = models.CharField(
        _('Status'), 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    # Регион для которого предназначен проект
    location_required = models.CharField(_('Location Required'), max_length=100, blank=True)
    is_remote = models.BooleanField(_('Remote Job'), default=True)
    
    # Опыт работы
    experience_required = models.CharField(_('Experience Required'), max_length=100, blank=True)
    
    # Видимость проекта
    is_private = models.BooleanField(_('Private Project'), default=False, help_text=_('Private projects are only visible to invited freelancers'))
    
    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('jobs:project_detail', args=[self.pk])
    
    @property
    def is_open(self):
        return self.status == 'open'
    
    @property
    def is_expired(self):
        if self.deadline:
            return self.deadline < timezone.now()
        return False

class Proposal(models.Model):
    """
    Предложение от фрилансера на проект
    """
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
        ('withdrawn', _('Withdrawn')),
    )
    
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='freelancer_proposals'
    )
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='proposals'
    )
    cover_letter = models.TextField(_('Cover Letter'))
    bid_amount = models.DecimalField(_('Bid Amount'), max_digits=10, decimal_places=2)
    delivery_time = models.PositiveIntegerField(_('Delivery Time (days)'))
    status = models.CharField(
        _('Status'), 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Proposal')
        verbose_name_plural = _('Proposals')
        ordering = ['-created_at']
        unique_together = ['freelancer', 'project']
        
    def __str__(self):
        return f"Proposal for {self.project.title} by {self.freelancer.username}"

class Contract(models.Model):
    """
    Контракт между фрилансером и клиентом
    """
    STATUS_CHOICES = (
        ('active', _('Active')),
        ('paused', _('Paused')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('disputed', _('Disputed')),
    )
    
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='client_contracts'
    )
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='freelancer_contracts'
    )
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='contracts'
    )
    proposal = models.OneToOneField(
        Proposal,
        on_delete=models.SET_NULL,
        related_name='contract',
        null=True,
        blank=True
    )
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    
    amount = models.DecimalField(_('Contract Amount'), max_digits=10, decimal_places=2)
    deadline = models.DateTimeField(_('Deadline'))
    
    status = models.CharField(
        _('Status'), 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active'
    )
    
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    # Автоматически сгенерированный уникальный номер контракта
    contract_id = models.CharField(
        _('Contract ID'), 
        max_length=20, 
        unique=True,
        editable=False
    )
    
    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Contract between {self.client.username} and {self.freelancer.username}"
    
    def save(self, *args, **kwargs):
        # Генерация уникального ID контракта если его нет
        if not self.contract_id:
            uid = str(uuid.uuid4()).split('-')[0]
            year = timezone.now().strftime('%Y')
            self.contract_id = f"KZ-{year}-{uid}"
        super().save(*args, **kwargs)

class Milestone(models.Model):
    """
    Этапы в контракте
    """
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('in_progress', _('In Progress')),
        ('submitted', _('Submitted')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('cancelled', _('Cancelled')),
    )
    
    contract = models.ForeignKey(
        Contract, 
        on_delete=models.CASCADE, 
        related_name='milestones'
    )
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    due_date = models.DateTimeField(_('Due Date'))
    
    status = models.CharField(
        _('Status'), 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Milestone')
        verbose_name_plural = _('Milestones')
        ordering = ['due_date']
        
    def __str__(self):
        return self.title
