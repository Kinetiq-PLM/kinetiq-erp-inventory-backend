from rest_framework import viewsets, generics
from .models import Products, ItemMasterData
from .serializers import ProductsSerializer, ItemMasterDataSerializer

class ProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

class ItemMasterDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ItemMasterData.objects.select_related('item')
    serializer_class = ItemMasterDataSerializer

class ProductItemMasterDataView(generics.RetrieveAPIView):
    queryset = Products.objects.prefetch_related('item_master_data')
    serializer_class = ProductsSerializer