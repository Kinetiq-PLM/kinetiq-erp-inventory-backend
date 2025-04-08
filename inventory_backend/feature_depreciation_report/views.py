from rest_framework import generics
from .models import DeprecationReport
from .serializers import (
    ProductDeprecationReportSerializer, 
    AssetsDeprecationReportSerializer, 
    RawMatDeprecationReportSerializer
)

class ProductDeprecationReportList(generics.ListCreateAPIView):
    serializer_class = ProductDeprecationReportSerializer

    def get_queryset(self):
        return DeprecationReport.objects.filter(
            inventory_item_id__productdocu_id__isnull=False  
        ).select_related(
            "inventory_item_id",
            "inventory_item_id__productdocu_id__product_id"
        ).values(
            "deprecation_report_id",
            "status",
            "reported_date",
            "content_id",
            "inventory_item_id__current_quantity",
            "inventory_item_id__productdocu_id",  
            "inventory_item_id__expiry",
            "inventory_item_id__productdocu_id__product_id__product_name",
        )


class AssetsDeprecationReportList(generics.ListCreateAPIView):
    serializer_class = AssetsDeprecationReportSerializer

    def get_queryset(self):
        return DeprecationReport.objects.filter(
            inventory_item_id__asset_id__isnull=False  
        ).select_related(
            "inventory_item_id",
            "inventory_item_id__asset_id",
        ).values(
            "deprecation_report_id",
            "status",
            "reported_date",
            "inventory_item_id",          
            "inventory_item_id__current_quantity",
            "inventory_item_id__asset_id",  
            "inventory_item_id__asset_id__asset_name",
        )


class RawMatDeprecationReportList(generics.ListCreateAPIView):
    serializer_class = RawMatDeprecationReportSerializer

    def get_queryset(self):
        return DeprecationReport.objects.filter(
            inventory_item_id__material_id__isnull=False  # Only include records where material_id is NOT NULL
        ).select_related(
            "inventory_item_id",
            "inventory_item_id__material_id",
           
        ).values(
            "deprecation_report_id",
            "status",
            "reported_date",
            "inventory_item_id",
            "inventory_item_id__current_quantity",
            "inventory_item_id__material_id",
            "inventory_item_id__material_id__material_name", 
        )
