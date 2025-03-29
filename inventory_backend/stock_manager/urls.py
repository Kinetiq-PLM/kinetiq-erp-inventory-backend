from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductsViewSet, AdminItemMasterDataViewSet,
    AssetsViewSet, RawMaterialsViewSet,
    PurchaseRequestViewSet
)

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'item-master-data', AdminItemMasterDataViewSet, basename='item-master-data')
router.register(r'assets', AssetsViewSet, basename='assets')
router.register(r'raw-materials', RawMaterialsViewSet, basename='raw-materials')
router.register(r'purchase-requests', PurchaseRequestViewSet, basename='purchase-requests')

urlpatterns = [
    path('', include(router.urls)),
]
