from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import (
    ItemMasterData, InventoryItem, InventoryItemThreshold,
    Purchase_requests, QuotationContent, PurchaseQuotation,
    ProductInventoryView, AssetInventoryView, RawMaterialInventoryView,
    WarehouseProductStockView, WarehouseAssetStockView, WarehouseMaterialStockView,
    WarehouseAllItemStockView
)
from .serializers import (
    AdminItemMasterDataSerializer,
    InventoryItemSerializer,
    InventoryItemThresholdSerializer,
    PurchaseRequestSerializer, QuotationContentSerializer, PurchaseQuotationSerializer,
    ProductInventoryViewSerializer, AssetInventoryViewSerializer, RawMaterialInventoryViewSerializer,
    WarehouseProductStockViewSerializer, WarehouseAssetStockViewSerializer, WarehouseMaterialStockViewSerializer,
    WarehouseAllItemStockViewSerializer
)
from django.db.models import F
from rest_framework.permissions import IsAuthenticated

# Use the specific DB View for ReadOnly operations on Products
class ProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WarehouseProductStockView.objects.all()
    serializer_class = WarehouseProductStockViewSerializer

    def get_queryset(self):
        queryset = WarehouseProductStockView.objects.all()

        item_id = self.request.query_params.get('item_id')
        if item_id:
            queryset = queryset.filter(item_id=item_id)
        
        warehouse_id = self.request.query_params.get('warehouse_id')
        if warehouse_id:
            queryset = queryset.filter(warehouse_id=warehouse_id)

        low_stock = self.request.query_params.get('low_stock')
        if low_stock is not None and low_stock.lower() == 'true':
            queryset = queryset.filter(available_stock__lt=F('minimum_threshold'), available_stock__gt=0)

        return queryset

# Use the InventoryItem model directly for Assets to get serial numbers
class AssetsViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = AssetInventoryView.objects.all() # Old: Using aggregated view
    serializer_class = InventoryItemSerializer # Use serializer that includes item_no

    def get_queryset(self):
        # Query InventoryItem directly, filtered by item_type='Asset'
        queryset = InventoryItem.objects.filter(item_type='Asset').select_related('item')

        # Add filtering if needed (e.g., by item master id)
        item_master_id = self.request.query_params.get('item_id')
        if item_master_id:
            queryset = queryset.filter(item__item_id=item_master_id)

        # Add filtering for low stock if meaningful for individual assets
        # (e.g., is_active=False could be considered 'Out of Stock'?
        # low_stock = self.request.query_params.get('low_stock', None)
        # if low_stock is not None and low_stock.lower() == 'true':
        #     # Implement appropriate logic for individual assets
        #     pass

        return queryset

# Use InventoryItem model directly for Raw Materials to get batch numbers
class RawMaterialsViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = RawMaterialInventoryView.objects.all() # Old: Using aggregated view
    serializer_class = InventoryItemSerializer # Use serializer that includes item_no

    def get_queryset(self):
        # Query InventoryItem directly, filtered by item_type='Raw Material'
        queryset = InventoryItem.objects.filter(item_type='Raw Material').select_related('item')

        # Add filtering if needed (e.g., by item master id)
        item_master_id = self.request.query_params.get('item_id')
        if item_master_id:
            queryset = queryset.filter(item__item_id=item_master_id)

        # Add filtering for low stock if needed - logic might need refinement for batches
        # low_stock = self.request.query_params.get('low_stock', None)
        # if low_stock is not None and low_stock.lower() == 'true':
            # How to define low stock for a batch? Maybe quantity < batch_min_threshold?
            # pass

        # Filter out items with zero quantity? Or rely on is_active?
        # queryset = queryset.filter(current_quantity__gt=0) 
        # queryset = queryset.filter(is_active=True)

        return queryset

# Changed to ModelViewSet to allow CUD operations
class AdminItemMasterDataViewSet(viewsets.ModelViewSet):
    queryset = ItemMasterData.objects.all()
    serializer_class = AdminItemMasterDataSerializer # Use updated serializer
    # Add filtering/searching as needed (e.g., by item_type)
    def get_queryset(self):
        queryset = ItemMasterData.objects.all()
        item_type = self.request.query_params.get('item_type')
        if item_type:
            # Assuming 'Product', 'Asset', 'Raw Material' are the valid strings
            queryset = queryset.filter(item_type=item_type)
        return queryset

# Renamed from InventoryItemDataViewSet and changed to ModelViewSet
class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer # Use updated serializer
    # Add filtering/searching as needed (e.g., by item_id from ItemMasterData)
    def get_queryset(self):
        queryset = InventoryItem.objects.all().select_related('item') # Optimize FK lookup
        item_master_id = self.request.query_params.get('item_id')
        warehouse_id = self.request.query_params.get('warehouse_id')
        item_no = self.request.query_params.get('item_no')

        if item_master_id:
            queryset = queryset.filter(item__item_id=item_master_id)
        if warehouse_id:
            queryset = queryset.filter(warehouse_id=warehouse_id)
        if item_no:
             queryset = queryset.filter(item_no=item_no)
        return queryset

# Changed to ModelViewSet
class InventoryItemThresholdViewSet(viewsets.ModelViewSet):
    queryset = InventoryItemThreshold.objects.all()
    serializer_class = InventoryItemThresholdSerializer # Use updated serializer
    # Add filtering/searching as needed
    def get_queryset(self):
        queryset = InventoryItemThreshold.objects.all().select_related('item') # Optimize FK lookup
        item_master_id = self.request.query_params.get('item_id')
        if item_master_id:
            queryset = queryset.filter(item__item_id=item_master_id)
        return queryset

class PurchaseRequestViewSet(viewsets.ModelViewSet):
    queryset = Purchase_requests.objects.all()
    serializer_class = PurchaseRequestSerializer # Serializer was updated

    # Default create/update/delete methods from ModelViewSet are likely sufficient
    # unless custom logic or ID generation is needed.
    # Removed explicit create/update methods for brevity unless needed.

class QuotationContentViewSet(viewsets.ModelViewSet):
    queryset = QuotationContent.objects.all()
    serializer_class = QuotationContentSerializer # Serializer was updated

class PurchaseQuotationViewSet(viewsets.ModelViewSet):
    queryset = PurchaseQuotation.objects.all()
    serializer_class = PurchaseQuotationSerializer # Serializer was updated

# --- Kept ViewSets for DB Views (ReadOnly) --- Updated filtering fields ---

class ProductInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing product inventory data using the database view.
    Provides aggregated stock levels.
    """
    queryset = ProductInventoryView.objects.all()
    serializer_class = ProductInventoryViewSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        queryset = ProductInventoryView.objects.all()

        # Filter by item_id if provided
        item_id = self.request.query_params.get('item_id', None) # Changed from product_id
        if item_id is not None:
            queryset = queryset.filter(item_id=item_id)

        # Filter by low stock (available_stock < minimum_threshold)
        low_stock = self.request.query_params.get('low_stock', None)
        if low_stock is not None and low_stock.lower() == 'true':
            queryset = queryset.filter(available_stock__lt=F('minimum_threshold'))

        return queryset

    # Default list/retrieve methods are likely sufficient
    # Removed explicit list/retrieve methods for brevity unless specific error handling needed

class AssetInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    DEPRECATED: Use AssetsViewSet which queries InventoryItem directly.
    This viewset remains temporarily for potential compatibility reasons
    but should ideally be removed if not used elsewhere.
    A viewset for viewing asset inventory data using the database view.
    """
    queryset = AssetInventoryView.objects.all()
    serializer_class = AssetInventoryViewSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        queryset = AssetInventoryView.objects.all()

        # Filter by item_id if provided
        item_id = self.request.query_params.get('item_id', None) # Changed from asset_id
        if item_id is not None:
            queryset = queryset.filter(item_id=item_id)

        # Filter by low stock (total_stock < minimum_threshold)
        low_stock = self.request.query_params.get('low_stock', None)
        if low_stock is not None and low_stock.lower() == 'true':
            # Note: Asset view doesn't have 'available_stock', using total_stock
            queryset = queryset.filter(total_stock__lt=F('minimum_threshold'))

        return queryset

    # Default list/retrieve methods are likely sufficient

class RawMaterialInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    DEPRECATED: Use RawMaterialsViewSet which queries InventoryItem directly.
    This viewset remains temporarily for potential compatibility reasons
    but should ideally be removed if not used elsewhere.
    A viewset for viewing raw material inventory data using the database view.
    """
    queryset = RawMaterialInventoryView.objects.all()
    serializer_class = RawMaterialInventoryViewSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        # ... (Keep filtering logic, but this viewset is deprecated)
        return super().get_queryset()

# --- WAREHOUSE SPECIFIC VIEW VIEWSETS ---

class WarehouseProductStockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides aggregated product stock levels per warehouse.
    Filter by item_id and/or warehouse_id.
    """
    queryset = WarehouseProductStockView.objects.all()
    serializer_class = WarehouseProductStockViewSerializer
    authentication_classes = [] # Adjust as needed
    permission_classes = [] # Adjust as needed

    def get_queryset(self):
        queryset = WarehouseProductStockView.objects.all()
        item_id = self.request.query_params.get('item_id', None)
        warehouse_id = self.request.query_params.get('warehouse_id', None)

        if item_id:
            queryset = queryset.filter(item_id=item_id)
        if warehouse_id:
            queryset = queryset.filter(warehouse_id=warehouse_id)

        return queryset

class WarehouseAssetStockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    DEPRECATED: Use WarehouseStockListView filtering by item_type='Asset'.
    Provides aggregated asset stock levels per warehouse.
    Filter by item_id and/or warehouse_id.
    """
    queryset = WarehouseAssetStockView.objects.all()
    serializer_class = WarehouseAssetStockViewSerializer
    authentication_classes = [] # Adjust as needed
    permission_classes = [] # Adjust as needed

    def get_queryset(self):
        queryset = WarehouseAssetStockView.objects.all()
        item_id = self.request.query_params.get('item_id', None)
        warehouse_id = self.request.query_params.get('warehouse_id', None)

        if item_id:
            queryset = queryset.filter(item_id=item_id)
        if warehouse_id:
            queryset = queryset.filter(warehouse_id=warehouse_id)

        return queryset

class WarehouseMaterialStockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    DEPRECATED: Use WarehouseStockListView filtering by item_type='Raw Material'.
    Provides aggregated material stock levels per warehouse.
    """
    queryset = WarehouseMaterialStockView.objects.all()
    serializer_class = WarehouseMaterialStockViewSerializer
    authentication_classes = [] # Adjust as needed
    permission_classes = [] # Adjust as needed

    def get_queryset(self):
        queryset = WarehouseMaterialStockView.objects.all()
        item_id = self.request.query_params.get('item_id', None)
        warehouse_id = self.request.query_params.get('warehouse_id', None)

        if item_id:
            queryset = queryset.filter(item_id=item_id)
        if warehouse_id:
            queryset = queryset.filter(warehouse_id=warehouse_id)

        return queryset

# --- COMBINED WAREHOUSE STOCK VIEW VIEWSET ---

class WarehouseAllItemStockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides combined aggregated stock levels for ALL item types per warehouse.
    Filter by item_id, warehouse_id, and/or item_type.
    """
    queryset = WarehouseAllItemStockView.objects.all()
    serializer_class = WarehouseAllItemStockViewSerializer
    authentication_classes = [] # Adjust as needed
    permission_classes = [] # Adjust as needed

    def get_queryset(self):
        queryset = WarehouseAllItemStockView.objects.all()
        item_id = self.request.query_params.get('item_id', None)
        warehouse_id = self.request.query_params.get('warehouse_id', None)
        item_type = self.request.query_params.get('item_type', None)

        if item_id:
            queryset = queryset.filter(item_id=item_id)
        if warehouse_id:
            queryset = queryset.filter(warehouse_id=warehouse_id)
        if item_type:
             # Ensure the item_type value matches 'Product', 'Asset', or 'Raw Material'
            queryset = queryset.filter(item_type=item_type)

        return queryset

class WarehouseStockListView(viewsets.ReadOnlyModelViewSet):
    """
    Provides combined aggregated stock levels for different item types per warehouse.
    Filter by warehouse_id and item_type.
    Handles Assets separately to return individual items with serial numbers.
    """
    # Default serializer - adjust if needed or handle in get_serializer_class
    serializer_class = WarehouseAllItemStockViewSerializer
    authentication_classes = [] # Adjust as needed
    permission_classes = [] # Adjust as needed

    def get_queryset(self):
        warehouse_id = self.request.query_params.get('warehouse_id')
        item_type = self.request.query_params.get('item_type')
        item_id = self.request.query_params.get('item_id')

        if not warehouse_id:
            return InventoryItem.objects.none() # Return empty queryset

        if item_type == 'Asset':
            queryset = InventoryItem.objects.filter(
                item_type='Asset',
                warehouse_id=warehouse_id
            ).select_related('item')
        elif item_type == 'Product':
            queryset = WarehouseProductStockView.objects.filter(warehouse_id=warehouse_id)
        elif item_type == 'Raw Material':
            # UPDATED: Query InventoryItem for Raw Materials too
            queryset = InventoryItem.objects.filter(
                item_type='Raw Material',
                warehouse_id=warehouse_id
            ).select_related('item')
            # Add filtering for active items if needed
            # queryset = queryset.filter(is_active=True)
            # queryset = queryset.filter(current_quantity__gt=0)
        else:
            return InventoryItem.objects.none() # Return empty if type invalid

        # Filter by item_id (master item id)
        if item_id:
             if item_type == 'Asset' or item_type == 'Raw Material':
                 queryset = queryset.filter(item__item_id=item_id)
             else: # Product uses view
                 queryset = queryset.filter(item_id=item_id)

        return queryset

    def get_serializer_class(self):
        item_type = self.request.query_params.get('item_type')

        if item_type == 'Asset':
            return InventoryItemSerializer
        elif item_type == 'Product':
            return WarehouseProductStockViewSerializer
        elif item_type == 'Raw Material':
            # UPDATED: Use InventoryItemSerializer for Raw Materials
            return InventoryItemSerializer
        else:
            raise serializers.ValidationError("Invalid or missing item_type specified.")

    # ... (keep context method if needed) ...