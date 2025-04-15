from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductsViewSet, AdminItemMasterDataViewSet,
    InventoryItemDataViewSet, InventoryItemThresholdViewSet,
    AssetsViewSet, RawMaterialsViewSet,
    PurchaseRequestViewSet, QuotationContentViewSet, PurchaseQuotationViewSet,
    ProductInventoryViewSet, AssetInventoryViewSet, RawMaterialInventoryViewSet
)

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'item-master-data', AdminItemMasterDataViewSet, basename='item-master-data')
router.register(r'inventory-item-data', InventoryItemDataViewSet, basename='inventory-item-data')
router.register(r'inventory-item-thresholds', InventoryItemThresholdViewSet, basename='inventory-item-thresholds')
router.register(r'assets', AssetsViewSet, basename='assets')
router.register(r'raw-materials', RawMaterialsViewSet, basename='raw-materials')
router.register(r'purchase-requests', PurchaseRequestViewSet, basename='purchase-requests')
router.register(r'quotation-contents', QuotationContentViewSet, basename='quotation-contents')
router.register(r'purchase-quotations', PurchaseQuotationViewSet, basename='purchase-quotations')
router.register(r'product-inventory', ProductInventoryViewSet, basename='product-inventory')
router.register(r'asset-inventory', AssetInventoryViewSet, basename='asset-inventory')
router.register(r'material-inventory', RawMaterialInventoryViewSet, basename='material-inventory')

urlpatterns = [
    path('', include(router.urls)),
]
