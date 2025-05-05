from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from assets.models import Asset

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get asset statistics
        context['total_assets'] = Asset.objects.count()
        context['available_assets'] = Asset.objects.filter(status='AVAILABLE').count()
        context['assigned_assets'] = Asset.objects.filter(status='ASSIGNED').count()
        context['under_maintenance_assets'] = Asset.objects.filter(
            status='IN_REPAIR'
        ).count()
        context['retired_assets'] = Asset.objects.filter(status='RETIRED').count()
        
        # Asset distribution by type
        context['asset_types'] = Asset.objects.values('asset_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Asset distribution by location
        context['locations'] = Asset.objects.values('location').annotate(
            count=Count('id')
        ).order_by('-count')

        # Asset distribution by make
        context['makes'] = Asset.objects.values('make').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Asset distribution by operating system with display values
        operating_systems = Asset.objects.values('operating_system').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Add display values for operating systems
        for os in operating_systems:
            for choice in Asset.OS_CHOICES:
                if choice[0] == os['operating_system']:
                    os['display_name'] = choice[1]
                    break
        context['operating_systems'] = operating_systems
        
        # Asset distribution by condition with display values
        conditions = Asset.objects.values('condition').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Add display values for conditions
        for condition in conditions:
            for choice in Asset.CONDITION_CHOICES:
                if choice[0] == condition['condition']:
                    condition['display_name'] = choice[1]
                    break
        context['conditions'] = conditions
        
        # Asset distribution by assignee (excluding unassigned)
        context['assignees'] = Asset.objects.exclude(
            assignee__isnull=True
        ).exclude(
            assignee__exact=''
        ).values('assignee').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Recent assets (last 5)
        context['recent_assets'] = Asset.objects.all().order_by('-registration_date')[:3]
        
        return context
