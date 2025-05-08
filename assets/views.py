from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import logging

from .models import Asset, AssetCheckout, AssetMovement
from .forms import AssetForm, AssetCheckoutForm, AssetMovementForm
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

@login_required
def checkout_asset(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    
    # Check if asset is already checked out
    if asset.status != 'AVAILABLE':
        messages.error(request, 'This asset is not available for checkout.')
        return redirect('asset-detail', pk=pk)
    
    if request.method == 'POST':
        form = AssetCheckoutForm(request.POST)
        if form.is_valid():
            checkout = form.save(commit=False)
            checkout.asset = asset
            checkout.checked_out_by = request.user
            checkout.save()
            
            # Update asset status
            asset.status = 'ASSIGNED'
            asset.assignee = request.user.email
            asset.save()
            
            messages.success(request, f'Asset {asset.asset_id} has been checked out successfully.')
            return redirect('asset-detail', pk=pk)
    else:
        form = AssetCheckoutForm()
    
    return render(request, 'assets/asset_checkout.html', {
        'form': form,
        'asset': asset
    })

@login_required
def checkin_asset(request, pk):
    checkout = get_object_or_404(AssetCheckout, pk=pk, status='CHECKED_OUT')
    asset = checkout.asset
    
    if request.method == 'POST':
        checkout.actual_return_date = timezone.now()
        checkout.status = 'RETURNED'
        checkout.save()
        
        # Update asset status
        asset.status = 'AVAILABLE'
        asset.assignee = None
        asset.save()
        
        messages.success(request, f'Asset {asset.asset_id} has been checked in successfully.')
        return redirect('asset-detail', pk=asset.pk)
    
    return render(request, 'assets/asset_checkin.html', {'checkout': checkout})

@login_required
def move_asset(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    
    if request.method == 'POST':
        form = AssetMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.asset = asset
            movement.moved_by = request.user
            movement.from_location = asset.location
            movement.save()
            
            # Update asset location
            asset.location = movement.to_location
            asset.save()
            
            messages.success(request, f'Asset {asset.asset_id} has been moved successfully.')
            return redirect('asset-detail', pk=pk)
    else:
        form = AssetMovementForm()
    
    return render(request, 'assets/asset_movement.html', {
        'form': form,
        'asset': asset
    })

@login_required
def asset_history(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    checkouts = asset.checkouts.all()
    movements = asset.movements.all()
    
    return render(request, 'assets/asset_history.html', {
        'asset': asset,
        'checkouts': checkouts,
        'movements': movements
    })
