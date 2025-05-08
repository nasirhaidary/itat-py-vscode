from django.urls import path
from .views import (
    AssetListView,
    AssetCreateView,
    AssetUpdateView,
    AssetDeleteView,
    AssetDetailView,
    checkout_asset,
    checkin_asset,
    move_asset,
    asset_history,
)

urlpatterns = [
    path('', AssetListView.as_view(), name='asset-list'),
    path('create/', AssetCreateView.as_view(), name='asset-create'),
    path('<int:pk>/', AssetDetailView.as_view(), name='asset-detail'),
    path('<int:pk>/update/', AssetUpdateView.as_view(), name='asset-update'),
    path('<int:pk>/delete/', AssetDeleteView.as_view(), name='asset-delete'),
    path('<int:pk>/checkout/', checkout_asset, name='asset-checkout'),
    path('checkin/<int:pk>/', checkin_asset, name='asset-checkin'),
    path('<int:pk>/move/', move_asset, name='asset-move'),
    path('<int:pk>/history/', asset_history, name='asset-history'),
]