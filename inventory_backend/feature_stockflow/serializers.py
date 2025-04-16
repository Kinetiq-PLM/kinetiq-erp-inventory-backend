# inventory/serializers.py
from rest_framework import serializers
from .models import Warehouse, InventoryItemData, WarehouseMovement, WarehouseMovementItem, WarehouseMovementData
from django.utils import timezone
from datetime import datetime
import uuid

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
            'warehouse_id',
            'warehouse_location'
        ]

        read_only_fields = fields  



class WarehouseMovementSerializer(serializers.ModelSerializer):
    docu_creation_date = serializers.DateTimeField(required=False)
    movement_date = serializers.DateTimeField(required=False)

    class Meta:
        model = WarehouseMovement
        fields = [
            'movement_id',            
            'docu_creation_date',
            'movement_date',
            'movement_status',
            'destination',
            'source',
            'comments'
        ]
        read_only_fields = ['movement_id'] 

    def create(self, validated_data):
        validated_data['docu_creation_date'] = validated_data.get('docu_creation_date', timezone.now())
        validated_data['movement_date'] = validated_data.get('movement_date', timezone.now())
        
        current_year = datetime.now().year
        
        if not validated_data.get('movement_id'):
            validated_data['movement_id'] = f"INV-WM-{current_year}-{uuid.uuid4().hex[:6].upper()}"
            
        movement = WarehouseMovement.objects.create(**validated_data)

        return movement
    
class WarehouseMovementItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseMovementItem
        fields = ['warehouse_movement_items_id', 'movement_id', 'inventory_item_id', 'quantity']
        read_only_fields = ['warehouse_movement_items_id'] 

    def create(self, validated_data):
        
        current_year = datetime.now().year
        custom_id = f"INV-WM-ITEM-{current_year}-{uuid.uuid4().hex[:8].upper()}"

        validated_data['warehouse_movement_items_id'] = custom_id

        return WarehouseMovementItem.objects.create(**validated_data)
    
class WarehouseMovementDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseMovementData
        fields = '__all__'