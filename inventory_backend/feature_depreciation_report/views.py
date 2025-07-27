from rest_framework import generics
from .models import ExpiryReportData
from .serializers import ExpiryReportDataSerializer

class ExpiryReportDataView(generics.ListCreateAPIView):
    queryset = ExpiryReportData.objects.all()
    serializer_class = ExpiryReportDataSerializer
    