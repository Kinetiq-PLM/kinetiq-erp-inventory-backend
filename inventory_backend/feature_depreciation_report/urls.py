# # inventory/urls.py
# from django.urls import path
# from .views import WarehouseMovementList, WarehouseList

# urlpatterns = [
#     path('warehouse-transfers/', WarehouseMovementList.as_view(), name='warehouse-transfers'),
#     path('warehouse-list/', WarehouseList.as_view(), name='warehouse-list'),
# ]


from django.urls import path
from .views import DepreciationReportList

urlpatterns = [
    path('depreciation-report/', DepreciationReportList.as_view(), name='depreciation-report-list'),
]