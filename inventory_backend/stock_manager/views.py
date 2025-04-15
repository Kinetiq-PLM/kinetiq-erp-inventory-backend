from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import (
    Product, ItemMasterData, InventoryItemData, InventoryItemThreshold,
    Asset, RawMaterial, Purchase_requests, QuotationContent, PurchaseQuotation,
    ProductInventoryView, AssetInventoryView
)
from .serializers import (
    ProductsSerializer, AdminItemMasterDataSerializer,
    InventoryItemDataSerializer, InventoryItemThresholdSerializer,
    AssetsSerializer, RawMaterialsSerializer,
    PurchaseRequestSerializer, QuotationContentSerializer, PurchaseQuotationSerializer,
    ProductInventoryViewSerializer, AssetInventoryViewSerializer
)
from django.db.models import F
from rest_framework.permissions import IsAuthenticated

class ProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

class AdminItemMasterDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ItemMasterData.objects.all()
    serializer_class = AdminItemMasterDataSerializer

class InventoryItemDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryItemData.objects.all()
    serializer_class = InventoryItemDataSerializer

class InventoryItemThresholdViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryItemThreshold.objects.all()
    serializer_class = InventoryItemThresholdSerializer

class AssetsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetsSerializer

class RawMaterialsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RawMaterial.objects.all()
    serializer_class = RawMaterialsSerializer

class PurchaseRequestViewSet(viewsets.ModelViewSet):
    queryset = Purchase_requests.objects.all()
    serializer_class = PurchaseRequestSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
            
        return Response(serializer.data)

class QuotationContentViewSet(viewsets.ModelViewSet):
    queryset = QuotationContent.objects.all()
    serializer_class = QuotationContentSerializer

class PurchaseQuotationViewSet(viewsets.ModelViewSet):
    queryset = PurchaseQuotation.objects.all()
    serializer_class = PurchaseQuotationSerializer

class ProductInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing product inventory data including committed stock and available stock
    """
    queryset = ProductInventoryView.objects.all()
    serializer_class = ProductInventoryViewSerializer
    # Allow both authenticated and unauthenticated users for testing
    authentication_classes = [] 
    permission_classes = []
    
    def get_queryset(self):
        # Add logging for debugging
        print("Fetching product inventory data")
        queryset = ProductInventoryView.objects.all()
        
        # Filter by product_id if provided
        product_id = self.request.query_params.get('product_id', None)
        if product_id is not None:
            queryset = queryset.filter(product_id__exact=product_id)
            
        # Filter by low stock (available_stock < minimum_threshold)
        low_stock = self.request.query_params.get('low_stock', None)
        if low_stock is not None and low_stock.lower() == 'true':
            queryset = queryset.filter(available_stock__lt=F('minimum_threshold'))
        
        # Log result count
        print(f"Found {queryset.count()} inventory items")
        return queryset
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve inventory data: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve inventory item: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AssetInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing asset inventory data including committed stock, on-order stock, and available stock
    """
    queryset = AssetInventoryView.objects.all()
    serializer_class = AssetInventoryViewSerializer
    # Allow both authenticated and unauthenticated users for testing
    authentication_classes = [] 
    permission_classes = []
    
    def get_queryset(self):
        # Add logging for debugging
        print("Fetching asset inventory data")
        queryset = AssetInventoryView.objects.all()
        
        # Filter by asset_id if provided
        asset_id = self.request.query_params.get('asset_id', None)
        if asset_id is not None:
            queryset = queryset.filter(asset_id__exact=asset_id)
            
        # Filter by low stock (available_stock < minimum_threshold)
        low_stock = self.request.query_params.get('low_stock', None)
        if low_stock is not None and low_stock.lower() == 'true':
            queryset = queryset.filter(available_stock__lt=F('minimum_threshold'))
        
        # Log result count
        print(f"Found {queryset.count()} asset inventory items")
        return queryset
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve asset inventory data: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve asset inventory item: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )