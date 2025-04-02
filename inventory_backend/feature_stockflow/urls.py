# inventory/urls.py
from django.urls import path
from .views import WarehouseMovementList, WarehouseItemsList, WarehouseList

urlpatterns = [
    path('warehouse-transfers/', WarehouseMovementList.as_view(), name='warehouse-transfers'),
    path('warehouse-item-list/', WarehouseItemsList.as_view(), name='warehouse-item-list'),
    path('warehouse-list/', WarehouseList.as_view, name='warehouse-list/')
]