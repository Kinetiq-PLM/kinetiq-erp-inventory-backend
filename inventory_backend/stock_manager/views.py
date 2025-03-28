from rest_framework import viewsets, generics
from .models import Products, ItemMasterData, Assets, Raw_materials
from .serializers import (
    ProductsSerializer, 
    ItemMasterDataSerializer, 
    AssetsSerializer, 
    RawMaterialsSerializer
)

class ProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

class ItemMasterDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ItemMasterData.objects.select_related('item')
    serializer_class = ItemMasterDataSerializer

class AssetsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Assets.objects.all()
    serializer_class = AssetsSerializer

class RawMaterialsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Raw_materials.objects.all()
    serializer_class = RawMaterialsSerializer

class ProductItemMasterDataView(generics.RetrieveAPIView):
    queryset = Products.objects.prefetch_related('item_master_data')
    serializer_class = ProductsSerializer
