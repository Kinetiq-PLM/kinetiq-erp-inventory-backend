from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import (
    ItemMasterData, InventoryItem, InventoryItemThreshold,
    Purchase_requests, QuotationContent, PurchaseQuotation,
    ProductInventoryView, AssetInventoryView, RawMaterialInventoryView
)
from .serializers import (
    AdminItemMasterDataSerializer,
    InventoryItemSerializer,
    InventoryItemThresholdSerializer,
    PurchaseRequestSerializer, QuotationContentSerializer, PurchaseQuotationSerializer,
    ProductInventoryViewSerializer, AssetInventoryViewSerializer, RawMaterialInventoryViewSerializer
)
from django.db.models import F
from rest_framework.permissions import IsAuthenticated

# Use the specific DB View for ReadOnly operations on Products
class ProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductInventoryView.objects.all()
    serializer_class = ProductInventoryViewSerializer
    # Define filtering/searching if needed based on ProductInventoryView fields

# Use the specific DB View for ReadOnly operations on Assets
class AssetsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AssetInventoryView.objects.all()
    serializer_class = AssetInventoryViewSerializer
    # Define filtering/searching if needed based on AssetInventoryView fields

# Use the specific DB View for ReadOnly operations on Raw Materials
class RawMaterialsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RawMaterialInventoryView.objects.all()
    serializer_class = RawMaterialInventoryViewSerializer
    # Define filtering/searching if needed based on RawMaterialInventoryView fields

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
    A viewset for viewing raw material inventory data using the database view.
    """
    queryset = RawMaterialInventoryView.objects.all()
    serializer_class = RawMaterialInventoryViewSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        queryset = RawMaterialInventoryView.objects.all()

        # Filter by item_id if provided
        item_id = self.request.query_params.get('item_id', None) # Changed from material_id
        if item_id is not None:
            queryset = queryset.filter(item_id=item_id)

        # Filter by low stock (total_stock < minimum_threshold)
        low_stock = self.request.query_params.get('low_stock', None)
        if low_stock is not None and low_stock.lower() == 'true':
             # Note: Material view doesn't have 'available_stock', using total_stock
            queryset = queryset.filter(total_stock__lt=F('minimum_threshold'))

        return queryset

    # Default list/retrieve methods are likely sufficient