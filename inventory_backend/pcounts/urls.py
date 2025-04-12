from django.urls import path
from .views import CyclicCountList, WarehouseList

urlpatterns = [
    path('cyclic_counts/', CyclicCountList.as_view(), name='cyclic_count_list'),
    path('warehouses/', WarehouseList.as_view(), name='warehouse_list'),
]
