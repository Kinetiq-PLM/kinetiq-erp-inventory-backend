# inventory/views.py
from rest_framework import generics
from .models import WarehouseMovement
from .serializers import WarehouseMovementSerializer

class WarehouseMovementList(generics.ListAPIView):
    queryset = WarehouseMovement.objects.all()
    serializer_class = WarehouseMovementSerializer