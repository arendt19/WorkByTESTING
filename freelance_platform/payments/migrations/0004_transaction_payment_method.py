# Generated by Django 5.1.7 on 2025-05-24 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_add_escrow_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='payment_method',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Payment Method'),
        ),
    ]
