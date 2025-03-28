# inventory/views.py
from rest_framework import generics
from .models import WarehouseMovement, Warehouse
from .serializers import WarehouseMovementSerializer, WarehouseSerializer

class WarehouseMovementList(generics.ListAPIView):
    queryset = WarehouseMovement.objects.all()
    serializer_class = WarehouseMovementSerializer

class WarehouseList(generics.ListAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer