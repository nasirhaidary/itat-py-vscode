from django.urls import path
from .views import (
    AssetListView,
    AssetCreateView,
    AssetUpdateView,
    AssetDeleteView,
)

urlpatterns = [
    path('', AssetListView.as_view(), name='asset-list'),
    path('create/', AssetCreateView.as_view(), name='asset-create'),
    path('<int:pk>/update/', AssetUpdateView.as_view(), name='asset-update'),
    path('<int:pk>/delete/', AssetDeleteView.as_view(), name='asset-delete'),
]