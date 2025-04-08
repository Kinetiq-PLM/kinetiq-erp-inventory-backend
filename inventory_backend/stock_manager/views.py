from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import (
    Product, ItemMasterData, InventoryItemData, InventoryItemThreshold,
    Asset, RawMaterial, Purchase_requests
)
from .serializers import (
    ProductsSerializer, AdminItemMasterDataSerializer,
    InventoryItemDataSerializer, InventoryItemThresholdSerializer,
    AssetsSerializer, RawMaterialsSerializer,
    PurchaseRequestSerializer
)

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