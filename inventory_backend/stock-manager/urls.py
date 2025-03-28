from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductsViewSet, ItemMasterDataViewSet, ProductItemMasterDataView

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'item-master-data', ItemMasterDataViewSet, basename='item-master-data')

urlpatterns = [
    path('', include(router.urls)),
    path('product/<str:pk>/item-master-data/', ProductItemMasterDataView.as_view(), name='product-item-master-data'),
]