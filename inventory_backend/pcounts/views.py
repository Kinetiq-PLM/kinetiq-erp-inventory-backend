from rest_framework import generics
from .models import CyclicCount
from .serializers import CyclicCountSerializer
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

class CyclicCountList(generics.ListCreateAPIView):
    serializer_class = CyclicCountSerializer

    def get_queryset(self):
        return CyclicCount.objects.select_related('employee', 'inventory_item').all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        logger.info(f"Created cyclic count record: {serializer.data}")
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data)
