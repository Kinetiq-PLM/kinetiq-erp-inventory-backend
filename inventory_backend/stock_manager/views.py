from rest_framework import viewsets, generics
from .models import Products, AdminItemMasterData, Assets, Raw_Materials
from .serializers import (
    ProductsSerializer,
    AdminItemMasterDataSerializer,
    AssetsSerializer,
    RawMaterialsSerializer
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

# Optional: If you need a view to retrieve products along with their item master data details.
class ProductAdminItemDataView(generics.RetrieveAPIView):
    queryset = Products.objects.all().prefetch_related('admin_item')
    serializer_class = ProductsSerializer
