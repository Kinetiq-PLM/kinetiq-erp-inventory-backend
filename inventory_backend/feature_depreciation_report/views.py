from rest_framework import generics
from .models import DeprecationReport
from .serializers import DeprecationReportSerializer

class DeprecationReportList(generics.ListCreateAPIView):
    serializer_class = DeprecationReportSerializer

    def get_queryset(self):
        return DeprecationReport.objects.select_related(
            "content_id__productdocu_id",
            "content_id__asset_id",
            "content_id__material_id",
        ).values(
            "deprecation_report_id",
            "status",
            "reported_date",
            "content_id",
            "content_id__asset_id",  
            "content_id__asset_id__asset_name",
            "content_id__material_id",
            "content_id__material_id__material_name",
            "content_id__productdocu_id",  
            "content_id__productdocu_id__expiry_date"  # Directly fetch expiry_date
        )




    # queryset = WarehouseMovement.objects.all()
    # serializer_class = WarehouseMovementSerializer

