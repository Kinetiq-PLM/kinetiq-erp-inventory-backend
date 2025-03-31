from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import (
    Products, AdminItemMasterData, InventoryItemData, InventoryProductData,
    Assets, Raw_Materials, Purchase_requests
)
from .serializers import (
    ProductsSerializer, AdminItemMasterDataSerializer,
    InventoryItemDataSerializer, InventoryProductDataSerializer,
    AssetsSerializer, RawMaterialsSerializer,
    PurchaseRequestSerializer
)

class ProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

class AdminItemMasterDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdminItemMasterData.objects.all()
    serializer_class = AdminItemMasterDataSerializer

class InventoryItemDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryItemData.objects.all()
    serializer_class = InventoryItemDataSerializer

class InventoryProductDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryProductData.objects.all()
    serializer_class = InventoryProductDataSerializer

class AssetsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Assets.objects.all()
    serializer_class = AssetsSerializer

class RawMaterialsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Raw_Materials.objects.all()
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
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
            
        return Response(serializer.data)