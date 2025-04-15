# # inventory/urls.py
# from django.urls import path
# from .views import WarehouseMovementList, WarehouseList

# urlpatterns = [
#     path('warehouse-transfers/', WarehouseMovementList.as_view(), name='warehouse-transfers'),
#     path('warehouse-list/', WarehouseList.as_view(), name='warehouse-list'),
# ]


from django.urls import path
from .views import  ExpiryReportList

urlpatterns = [
    # path('product-depreciation-report/', ProductDeprecationReportList.as_view(), name='product-depreciation-report'),
    # path('assets-depreciation-report/', AssetsDeprecationReportList.as_view(), name='assets-depreciation-report'),
    # path('raw-material-depreciation-report/', RawMatDeprecationReportList.as_view(), name='raw-material-depreciation-report'),
    path('expiry-report/', ExpiryReportList.as_view(), name='expiry-report'),
]