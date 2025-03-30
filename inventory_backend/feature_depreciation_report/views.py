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
            content_id__productdocu_id__isnull=False  
        ).select_related(
            "content_id__productdocu_id"
        ).values(
            "deprecation_report_id",
            "status",
            "reported_date",
            "content_id",
            "content_id__productdocu_id",  
            "content_id__productdocu_id__expiry_date",
        )


class AssetsDeprecationReportList(generics.ListCreateAPIView):
    serializer_class = AssetsDeprecationReportSerializer

    def get_queryset(self):
        return DeprecationReport.objects.filter(
            content_id__asset_id__isnull=False  
        ).select_related(
            "content_id__asset_id"
        ).values(
            "deprecation_report_id",
            "status",
            "reported_date",
            "content_id",
            "content_id__asset_id",  
            "content_id__asset_id__asset_name",
        )


class RawMatDeprecationReportList(generics.ListCreateAPIView):
    serializer_class = RawMatDeprecationReportSerializer

    def get_queryset(self):
        return DeprecationReport.objects.filter(
            content_id__material_id__isnull=False  # Only include records where material_id is NOT NULL
        ).select_related(
            "content_id__material_id"
        ).values(
            "deprecation_report_id",
            "status",
            "reported_date",
            "content_id",
            "content_id__material_id",
            "content_id__material_id__material_name", 
        )
