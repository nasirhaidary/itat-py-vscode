# Generated by Django 5.2 on 2025-05-05 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_alter_asset_asset_type_alter_asset_condition_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='ram_unit',
            field=models.CharField(choices=[('MB', 'MB'), ('GB', 'GB'), ('TB', 'TB')], default='GB', max_length=2),
        ),
        migrations.AddField(
            model_name='asset',
            name='storage_unit',
            field=models.CharField(choices=[('MB', 'MB'), ('GB', 'GB'), ('TB', 'TB')], default='GB', max_length=2),
        ),
    ]
