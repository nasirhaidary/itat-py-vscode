from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

from .models import Asset
from .forms import AssetForm
from .filters import AssetFilter

logger = logging.getLogger(__name__)

class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = 'assets/asset_list.html'
    context_object_name = 'assets'
    paginate_by = 10

    def get_queryset(self):
        queryset = Asset.objects.all()
        self.filterset = AssetFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

class AssetCreateView(LoginRequiredMixin, CreateView):
    model = Asset
    form_class = AssetForm
    template_name = 'assets/asset_form.html'
    success_url = reverse_lazy('asset-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f'Asset created: {self.object.asset_id} by {self.request.user}')
        messages.success(self.request, 'Asset created successfully.')
        return response

class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = 'assets/asset_form.html'
    success_url = reverse_lazy('asset-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f'Asset updated: {self.object.asset_id} by {self.request.user}')
        messages.success(self.request, 'Asset updated successfully.')
        return response

class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = Asset
    template_name = 'assets/asset_confirm_delete.html'
    success_url = reverse_lazy('asset-list')

    def delete(self, request, *args, **kwargs):
        asset = self.get_object()
        logger.info(f'Asset deleted: {asset.asset_id} by {request.user}')
        messages.success(request, 'Asset deleted successfully.')
        return super().delete(request, *args, **kwargs)

class AssetDetailView(LoginRequiredMixin, DetailView):
    model = Asset
    template_name = 'assets/asset_detail.html'
    context_object_name = 'asset'
