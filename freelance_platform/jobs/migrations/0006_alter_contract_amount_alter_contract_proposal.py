# Generated by Django 5.1.8 on 2025-05-21 12:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_remove_milestone_is_escrow_funded_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='proposal',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contract', to='jobs.proposal'),
        ),
    ]
