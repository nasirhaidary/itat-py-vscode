from django.db import migrations

def update_new_condition(apps, schema_editor):
    Asset = apps.get_model('assets', 'Asset')
    Asset.objects.filter(condition='NEW').update(condition='WORKING')

class Migration(migrations.Migration):
    dependencies = [
        ('assets', '0005_asset_ram_unit_asset_storage_unit'),
    ]

    operations = [
        migrations.RunPython(update_new_condition),
    ]