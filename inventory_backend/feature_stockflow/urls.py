# inventory/urls.py
from django.urls import path
from .views import WarehouseList, InventoryItemDataList, WarehouseMovementCreateView, WarehouseMovementItemCreateView, WarehouseMovementDataListView

urlpatterns = [
  
    path('warehouse-item-list/', InventoryItemDataList.as_view(), name='warehouse-item-list'),
    path('warehouse-list/', WarehouseList.as_view(), name='warehouse-list'),
    path('warehousemovement-transfer/', WarehouseMovementCreateView.as_view(), name='transfer-request'),
    path('warehousemovement-items/', WarehouseMovementItemCreateView.as_view(), name='warehousemovement-item'),
    path('warehousemovement-data/', WarehouseMovementDataListView.as_view(), name='warehousemovement-data'),
]