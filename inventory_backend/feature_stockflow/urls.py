# inventory/urls.py
from django.urls import path
from .views import WarehouseMovementList

urlpatterns = [
    path('warehouse-transfers/', WarehouseMovementList.as_view(), name='warehouse-transfers'),
]