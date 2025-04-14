from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CyclicCountList, WarehouseList, NotificationViewSet, InventoryItemList, UserList

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('cyclic_counts/', CyclicCountList.as_view(), name='cyclic_counts'),
    path('warehouses/', WarehouseList.as_view(), name='warehouse_list'),
    path('inventory-items/', InventoryItemList.as_view(), name='inventory_items_list'),
    path('users/', UserList.as_view(), name='user_list'),
    path('', include(router.urls)),
]
