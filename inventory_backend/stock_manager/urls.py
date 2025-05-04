from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductsViewSet, AdminItemMasterDataViewSet,
    InventoryItemViewSet, InventoryItemThresholdViewSet,
    AssetsViewSet, RawMaterialsViewSet,
    PurchaseRequestViewSet, QuotationContentViewSet, PurchaseQuotationViewSet,
    ProductInventoryViewSet, AssetInventoryViewSet, RawMaterialInventoryViewSet,
    WarehouseProductStockViewSet, WarehouseAssetStockViewSet, WarehouseMaterialStockViewSet,
    WarehouseAllItemStockViewSet
)

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'item-master-data', AdminItemMasterDataViewSet, basename='item-master-data')
router.register(r'inventory-items', InventoryItemViewSet, basename='inventory-items')
router.register(r'inventory-item-thresholds', InventoryItemThresholdViewSet, basename='inventory-item-thresholds')
router.register(r'assets', AssetsViewSet, basename='assets')
router.register(r'raw-materials', RawMaterialsViewSet, basename='raw-materials')
router.register(r'purchase-requests', PurchaseRequestViewSet, basename='purchase-requests')
router.register(r'quotation-contents', QuotationContentViewSet, basename='quotation-contents')
router.register(r'purchase-quotations', PurchaseQuotationViewSet, basename='purchase-quotations')
router.register(r'product-inventory', ProductInventoryViewSet, basename='product-inventory')
router.register(r'asset-inventory', AssetInventoryViewSet, basename='asset-inventory')
router.register(r'material-inventory', RawMaterialInventoryViewSet, basename='material-inventory')

# --- WAREHOUSE SPECIFIC STOCK VIEW ENDPOINTS ---
router.register(r'warehouse-stock/products', WarehouseProductStockViewSet, basename='warehouse-product-stock')
router.register(r'warehouse-stock/assets', WarehouseAssetStockViewSet, basename='warehouse-asset-stock')
router.register(r'warehouse-stock/materials', WarehouseMaterialStockViewSet, basename='warehouse-material-stock')

# --- COMBINED WAREHOUSE STOCK VIEW ENDPOINT ---
router.register(r'warehouse-stock/all-items', WarehouseAllItemStockViewSet, basename='warehouse-all-item-stock')

urlpatterns = [
    path('', include(router.urls)),
]
