# inventory/urls.py
from django.urls import path
from .views import WarehouseMovementList, WarehouseList, InventoryItemDataList

urlpatterns = [
    path('warehouse-transfers/', WarehouseMovementList.as_view(), name='warehouse-transfers'),
    path('warehouse-item-list/', InventoryItemDataList.as_view(), name='warehouse-item-list'),
    path('warehouse-list/', WarehouseList.as_view(), name='warehouse-list')
]