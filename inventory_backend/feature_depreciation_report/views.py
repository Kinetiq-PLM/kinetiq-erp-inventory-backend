from rest_framework import generics
from .models import DepreciationReport
from .serializers import DepreciationReportSerializer

class DepreciationReportList(generics.ListCreateAPIView):
    queryset = DepreciationReport.objects.all()
    serializer_class = DepreciationReportSerializer



    # queryset = WarehouseMovement.objects.all()
    # serializer_class = WarehouseMovementSerializer

