# inventory/views.py
from rest_framework import generics
from .models import Warehouse, InventoryItemData, WarehouseMovementData
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Case, When, Value, F, CharField, DateField
from .serializers import WarehouseSerializer, InventoryItemDataSerializer, WarehouseMovementSerializer, WarehouseMovementItemSerializer, WarehouseMovementDataSerializer




# Warehouse Table
class WarehouseList(generics.ListAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

# View for Each Item Data in Inventory 
class InventoryItemDataList(generics.ListAPIView):
    queryset = InventoryItemData.objects.all()
    serializer_class = InventoryItemDataSerializer

class WarehouseMovementCreateView(APIView):
    def post(self, request):
        serializer = WarehouseMovementSerializer(data=request.data)
        if serializer.is_valid():
            movement = serializer.save()
            return Response(WarehouseMovementSerializer(movement).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WarehouseMovementItemCreateView(APIView):
    def post(self, request):
        serializer = WarehouseMovementItemSerializer(data=request.data)
        if serializer.is_valid():
            # Save the warehouse movement item, with custom ID
            warehouse_movement_item = serializer.save()
            return Response(WarehouseMovementItemSerializer(warehouse_movement_item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WarehouseMovementDataListView(generics.ListAPIView):
    queryset = WarehouseMovementData.objects.all()
    serializer_class = WarehouseMovementDataSerializer


    
# OLD LOGIC (FOR BACKUP)

# class WarehouseItemsList(generics.ListCreateAPIView):
#     def get_queryset(self):
#         return DocumentItem.objects.filter(
#             warehouse_id__isnull=False  
#         ).select_related(
#             "item_id__asset_id",
#             "material_id",
#             "productdocu_id__product_id",
#             "warehouse_id",
#         ).annotate(
            
#             type=Case(
#                 When(material_id__isnull=False, then=Value("Raw Material")),
#                 When(item_id__isnull=False, then=Value("Asset")),
#                 When(productdocu_id__isnull=False, then=Value("Product")),
#                 default=Value("Unknown"),
#                 output_field=CharField()
#             ),
            
#             item_name=Case(
#                 When(material_id__isnull=False, then=F("material_id__material_name")),
#                 When(item_id__isnull=False, then=F("item_id__asset_id__asset_name")),
#                 When(productdocu_id__isnull=False, then=F("productdocu_id__product_id__product_name")),
#                 default=Value("Unknown"),
#                 output_field=CharField()
#             ),

#             item_management=Case(
#                 When(batch_no__isnull=False, then=Value("Batch No")),
#                 When(serial_id__isnull=False, then=Value("Serial Id")),
#                 default=Value("Unknown"),
#                 output_field=CharField()
#             ),

#             identifier=Case(
#                 When(batch_no__isnull=False, then=F("batch_no")),
#                 When(serial_id__isnull=False, then=F("serial_id")),
#                 default=Value("Unknown"),
#                 output_field=CharField()
#             ),

#             expiry_date=Case(
#                 # When(material_id__isnull=False, then=F("material_id__expiry_date")),
#                 # When(asset_id__isnull=False, then=F("asset_id__expiry_date")),
#                 When(productdocu_id__isnull=False, then=F("productdocu_id__expiry_date")),
#                 default=Value(None, output_field=DateField()),
#                 output_field=DateField()
#             )


#         ).values(
#             "content_id",
#             "item_name",
#             "type",
#             "item_management",
#             "identifier",
#             "expiry_date",
#             "quantity",
#             "warehouse_id__warehouse_location",
            
#         )
#     serializer_class = WarehouseItemListSerializer