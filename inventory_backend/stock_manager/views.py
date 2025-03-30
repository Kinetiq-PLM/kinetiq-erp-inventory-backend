from rest_framework import viewsets, generics
from .models import (
    Products, AdminItemMasterData, InventoryItemMasterData,
    Assets, Raw_Materials, Purchase_requests
)
from .serializers import (
    ProductsSerializer, AdminItemMasterDataSerializer,
    AssetsSerializer, RawMaterialsSerializer,
    PurchaseRequestSerializer
)

class ProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

class AdminItemMasterDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdminItemMasterData.objects.all()
    serializer_class = AdminItemMasterDataSerializer

class AssetsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Assets.objects.all()
    serializer_class = AssetsSerializer

class RawMaterialsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Raw_Materials.objects.all()
    serializer_class = RawMaterialsSerializer

class PurchaseRequestViewSet(viewsets.ModelViewSet):
    queryset = Purchase_requests.objects.all()
    serializer_class = PurchaseRequestSerializer
