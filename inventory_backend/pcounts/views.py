from rest_framework import generics
from .models import CyclicCount
from .serializers import CyclicCountSerializer
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

class CyclicCountList(generics.ListAPIView):
    serializer_class = CyclicCountSerializer

    def get_queryset(self):
        queryset = CyclicCount.objects.select_related(
            'product_data__inventory_item__item__product',
            'employee'
        ).all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for item in data:
            logger.info(f"Item: {item['inventory_count_id']}, Product Name: {item.get('product_name')}")
        return Response(data)