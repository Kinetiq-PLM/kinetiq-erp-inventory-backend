# inventory/views.py
from rest_framework import generics
from .models import WarehouseMovement, DocumentItem, Warehouse
from django.db.models import Case, When, Value, F, CharField, DateField
from .serializers import WarehouseMovementSerializer, WarehouseItemListSerializer, WarehouseSerializer


class WarehouseMovementList(generics.ListAPIView):
    queryset = WarehouseMovement.objects.all()
    serializer_class = WarehouseMovementSerializer


class WarehouseItemsList(generics.ListCreateAPIView):
    def get_queryset(self):
        return DocumentItem.objects.filter(
            warehouse_id__isnull=False  
        ).select_related(
            "item_id__asset_id",
            "material_id",
            "productdocu_id__product_id",
            "warehouse_id",
        ).annotate(
            
            type=Case(
                When(material_id__isnull=False, then=Value("Raw Material")),
                When(item_id__isnull=False, then=Value("Asset")),
                When(productdocu_id__isnull=False, then=Value("Product")),
                default=Value("Unknown"),
                output_field=CharField()
            ),
            
            item_name=Case(
                When(material_id__isnull=False, then=F("material_id__material_name")),
                When(item_id__isnull=False, then=F("item_id__asset_id__asset_name")),
                When(productdocu_id__isnull=False, then=F("productdocu_id__product_id__product_name")),
                default=Value("Unknown"),
                output_field=CharField()
            ),

            item_management=Case(
                When(batch_no__isnull=False, then=Value("Batch No")),
                When(serial_id__isnull=False, then=Value("Serial Id")),
                default=Value("Unknown"),
                output_field=CharField()
            ),

            identifier=Case(
                When(batch_no__isnull=False, then=F("batch_no")),
                When(serial_id__isnull=False, then=F("serial_id")),
                default=Value("Unknown"),
                output_field=CharField()
            ),

            expiry_date=Case(
                # When(material_id__isnull=False, then=F("material_id__expiry_date")),
                # When(asset_id__isnull=False, then=F("asset_id__expiry_date")),
                When(productdocu_id__isnull=False, then=F("productdocu_id__expiry_date")),
                default=Value(None, output_field=DateField()),
                output_field=DateField()
            )


        ).values(
            "content_id",
            "item_name",
            "type",
            "item_management",
            "identifier",
            "expiry_date",
            "quantity",
            "warehouse_id__warehouse_location",
            
        )
    serializer_class = WarehouseItemListSerializer

class WarehouseList(generics.ListAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer