from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductsViewSet, 
    ItemMasterDataViewSet, 
    AssetsViewSet, 
    RawMaterialsViewSet
)

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'item-master-data', ItemMasterDataViewSet, basename='item-master-data')
router.register(r'assets', AssetsViewSet, basename='assets')
router.register(r'raw-materials', RawMaterialsViewSet, basename='raw-materials')

urlpatterns = [
    path('', include(router.urls)),
]
