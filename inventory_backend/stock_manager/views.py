from rest_framework import viewsets
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
