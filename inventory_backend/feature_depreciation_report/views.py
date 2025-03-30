from rest_framework import generics
from .models import DeprecationReport
from .serializers import DeprecationReportSerializer

class DepreciationReportList(generics.ListCreateAPIView):
    queryset = DeprecationReport.objects.all()
    serializer_class = DeprecationReportSerializer



    # queryset = WarehouseMovement.objects.all()
    # serializer_class = WarehouseMovementSerializer

