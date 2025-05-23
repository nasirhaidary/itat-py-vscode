# Generated by Django 5.2 on 2025-05-04 12:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_alter_asset_asset_type_alter_asset_assignee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='asset_type',
            field=models.CharField(choices=[('LAPTOP', 'Laptop'), ('DESKTOP', 'Desktop'), ('MOBILE', 'Mobile'), ('TABLET', 'Tablet'), ('PRINTER', 'Printer'), ('SCANNER', 'Scanner'), ('PROJECTOR', 'Projector'), ('SERVER', 'Server'), ('NETWORK_DEVICE', 'Network Device'), ('MONITOR', 'Monitor'), ('SCREEN', 'Screen'), ('TV', 'tv'), ('ROBOTS', 'Robots'), ('UPS', 'UPS'), ('EXTERNAL_DRIVE', 'External Drive'), ('OTHER', 'Other')], max_length=100),
        ),
        migrations.AlterField(
            model_name='asset',
            name='processor',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='asset',
            name='ram',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='asset',
            name='storage',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
