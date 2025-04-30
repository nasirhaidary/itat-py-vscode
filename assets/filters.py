import django_filters
from .models import Asset

class AssetFilter(django_filters.FilterSet):
    asset_id = django_filters.CharFilter(lookup_expr='icontains')
    asset_type = django_filters.CharFilter(lookup_expr='icontains')
    make = django_filters.CharFilter(lookup_expr='icontains')
    model = django_filters.CharFilter(lookup_expr='icontains')
    serial_number = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    assignee = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Asset.STATUS_CHOICES)
    condition = django_filters.ChoiceFilter(choices=Asset.CONDITION_CHOICES)

    class Meta:
        model = Asset
        fields = ['asset_id', 'asset_type', 'make', 'model', 'serial_number', 
                 'location', 'status', 'assignee', 'condition']