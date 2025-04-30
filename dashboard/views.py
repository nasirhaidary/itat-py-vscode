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
        context['active_assets'] = Asset.objects.filter(status='ACTIVE').count()
        context['maintenance_assets'] = Asset.objects.filter(status='MAINTENANCE').count()
        context['inactive_assets'] = Asset.objects.filter(status='INACTIVE').count()
        
        # Asset distribution by type
        context['asset_types'] = Asset.objects.values('asset_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Asset distribution by location
        context['locations'] = Asset.objects.values('location').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Asset condition summary
        context['conditions'] = Asset.objects.values('condition').annotate(
            count=Count('id')
        ).order_by('condition')
        
        # Recent assets (last 5)
        context['recent_assets'] = Asset.objects.all().order_by('-registration_date')[:5]
        
        return context
