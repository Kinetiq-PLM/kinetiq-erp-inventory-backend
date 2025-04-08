# inventory/serializers.py
from rest_framework import serializers
from .models import WarehouseMovement, Warehouse, InventoryItemData

class WarehouseMovementSerializer(serializers.ModelSerializer):
    item = serializers.CharField(source='item.item_id')  # Display item_id
    destination = serializers.CharField(source='destination.warehouse_id')  # Display warehouse_id
    source = serializers.CharField(source='source.warehouse_id')  # Display warehouse_id
    reference_id_purchase_order = serializers.CharField(
        source='reference_id_purchase_order.purchase_id', allow_null=True
    )
    reference_id_order = serializers.CharField(
        source='reference_id_order.order_id', allow_null=True
    )

    class Meta:
        model = WarehouseMovement
        fields = [
            'movement_id',
            'item',
            'movement_type',
            'quantity',
            'movement_date',
            'destination',
            'source',
            'reference_id_purchase_order',
            'reference_id_order',
        ]

# class WarehouseItemListSerializer(serializers.Serializer):
#     item_name = serializers.CharField()
#     item_management = serializers.CharField()
#     type = serializers.CharField()
#     identifier = serializers.CharField()
#     expiry_date = serializers.DateField()
#     quantity = serializers.IntegerField()
#     content_id = serializers.CharField()
#     warehouse_location = serializers.CharField()
    
class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['warehouse_id', 'warehouse_location']  

class InventoryItemDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItemData
        fields = [
            'inventory_item_id',
            'item_type',
            'item_name',
            'item_management',
            'item_management_id',
            'current_quantity',
            'shelf_life',
            'expiry',
            'warehouse_location'
        ]

        read_only_fields = fields  # Since it's a view, all fields are read-only