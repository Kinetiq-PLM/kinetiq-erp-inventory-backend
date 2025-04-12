from rest_framework import generics
from .models import CyclicCount, InventoryItem
from .serializers import CyclicCountSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
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

class WarehouseList(APIView):
    """
    View to list all available warehouse IDs.
    """
    def get(self, request, format=None):
        # Get unique warehouse IDs from inventory items
        warehouses = InventoryItem.objects.values_list('warehouse_id', flat=True).distinct()
        # Filter out None/empty values and convert to list
        warehouse_list = [w for w in warehouses if w]
        return Response(warehouse_list)
