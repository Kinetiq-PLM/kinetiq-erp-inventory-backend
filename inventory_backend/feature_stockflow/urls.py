# inventory/urls.py
from django.urls import path
from .views import WarehouseMovementList, WarehouseList

urlpatterns = [
    path('warehouse-transfers/', WarehouseMovementList.as_view(), name='warehouse-transfers'),
    path('warehouse-list/', WarehouseList.as_view(), name='warehouse-list'),
]