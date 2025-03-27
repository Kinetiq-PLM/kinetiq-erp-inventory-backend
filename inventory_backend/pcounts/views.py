from rest_framework import generics
from .models import CyclicCount
from .serializers import CyclicCountSerializer

class CyclicCountList(generics.ListAPIView):
    serializer_class = CyclicCountSerializer

    def get_queryset(self):
        return CyclicCount.objects.select_related(
            'item_md__item', 
            'employee'        
        ).all()
