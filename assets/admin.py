from django.contrib import admin
from .models import Asset

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_id', 'asset_type', 'make', 'model', 'status', 'assignee', 'condition']
    list_filter = ['status', 'condition', 'asset_type', 'location']
    search_fields = ['asset_id', 'serial_number', 'assignee']
    ordering = ['-registration_date']