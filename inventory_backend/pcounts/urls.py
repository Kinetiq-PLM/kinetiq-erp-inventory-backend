from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CyclicCountList, WarehouseList, NotificationViewSet, InventoryItemList

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('cyclic_counts/', CyclicCountList.as_view(), name='cyclic_count_list'),
    path('warehouses/', WarehouseList.as_view(), name='warehouse_list'),
    path('inventory-items/', InventoryItemList.as_view(), name='inventory_item_list'),
    path('', include(router.urls)),
]
