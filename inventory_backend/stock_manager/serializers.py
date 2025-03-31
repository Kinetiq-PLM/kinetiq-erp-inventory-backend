from rest_framework import serializers
from .models import (
    Products, AdminItemMasterData, InventoryItemData, InventoryProductData,
    Assets, Raw_Materials, Purchase_requests
)
import logging

logger = logging.getLogger(__name__)

class AdminItemMasterDataSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)

    class Meta:
        model = AdminItemMasterData
        fields = [
            'item_id',
            'product_name'
        ]

class InventoryItemDataSerializer(serializers.ModelSerializer):
    item_id = serializers.CharField(source='admin_item.item_id', read_only=True)

    class Meta:
        model = InventoryItemData
        fields = [
            'inventory_item_id',
            'item_id',
            'minimum_threshold',
            'maximum_threshold',
            'total_stock',
            'available_stock',
            'last_update'
        ]

class InventoryProductDataSerializer(serializers.ModelSerializer):
    inventory_item_id = serializers.CharField(source='inventory_item.inventory_item_id', read_only=True)
    item_id = serializers.CharField(source='inventory_item.admin_item.item_id', read_only=True)

    class Meta:
        model = InventoryProductData
        fields = [
            'item_md_id',
            'inventory_item_id',
            'item_id',
            'stock_on_order',
            'stock_committed'
        ]

class ProductsSerializer(serializers.ModelSerializer):
    item_id = serializers.CharField(source='item.item_id', read_only=True)
    admin_item = AdminItemMasterDataSerializer(source='item', read_only=True)
    inventory_data = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = [
            'product_id',
            'item',
            'item_id',
            'product_name',
            'admin_item',
            'inventory_data'
        ]

    def get_inventory_data(self, obj):
        try:
            inventory_item = InventoryItemData.objects.filter(admin_item=obj.item).first()
            
            data = {}
            
            if inventory_item:
                data["item_id"] = inventory_item.admin_item.item_id
                data["total_stock"] = inventory_item.total_stock
                data["available_stock"] = inventory_item.available_stock
                
                product_data = InventoryProductData.objects.filter(inventory_item=inventory_item).first()
                
                if product_data:
                    data["stock_on_order"] = product_data.stock_on_order
                    data["stock_committed"] = product_data.stock_committed
            
            return data
        except Exception as e:
            logger.error(f"Error merging inventory data for product {obj.product_id}: {str(e)}")
            return {}


class AssetsSerializer(serializers.ModelSerializer):
    item_id = serializers.CharField(source='item.item_id', read_only=True)
    inventory_data = serializers.SerializerMethodField()
    
    purchase_date = serializers.DateField(format="%Y-%m-%d", required=False)
    serial_no = serializers.CharField(required=False)

    class Meta:
        model = Assets
        fields = [
            'asset_id', 
            'item', 
            'item_id', 
            'asset_name', 
            'purchase_date',
            'serial_no',
            'inventory_data'
        ]

    def get_inventory_data(self, obj):
        if not obj.item:
            return {}
            
        try:
            inventory_item = InventoryItemData.objects.filter(
                admin_item_id=obj.item.item_id
            ).first()
            
            if not inventory_item:
                return {}
                
            return {
                'item_id': obj.item.item_id,
                'total_stock': inventory_item.total_stock,
                'available_stock': inventory_item.available_stock,
                'minimum_threshold': inventory_item.minimum_threshold,
                'maximum_threshold': inventory_item.maximum_threshold,
                'last_update': inventory_item.last_update
            }
        except Exception as e:
            logger.error(f"Error getting inventory data for asset {obj.asset_id}: {str(e)}")
            return {}

class RawMaterialsSerializer(serializers.ModelSerializer):
    item_id = serializers.CharField(source='item.item_id', read_only=True)
    inventory_data = serializers.SerializerMethodField()
    
    description = serializers.CharField(required=False)
    unit_of_measure = serializers.CharField(required=False)

    class Meta:
        model = Raw_Materials
        fields = [
            'material_id', 
            'item', 
            'item_id', 
            'material_name',
            'description',
            'unit_of_measure',
            'inventory_data'
        ]

    def get_inventory_data(self, obj):
        if not obj.item:
            return {}
            
        try:
            inventory_item = InventoryItemData.objects.filter(
                admin_item_id=obj.item.item_id
            ).first()
            
            if not inventory_item:
                return {}
                
            return {
                'item_id': obj.item.item_id,
                'total_stock': inventory_item.total_stock,
                'available_stock': inventory_item.available_stock,
                'minimum_threshold': inventory_item.minimum_threshold,
                'maximum_threshold': inventory_item.maximum_threshold,
                'last_update': inventory_item.last_update
            }
        except Exception as e:
            logger.error(f"Error getting inventory data for material {obj.material_id}: {str(e)}")
            return {}

class PurchaseRequestSerializer(serializers.ModelSerializer):
    material_details = RawMaterialsSerializer(source='material_id', read_only=True)
    asset_details = AssetsSerializer(source='asset_id', read_only=True)
    
    class Meta:
        model = Purchase_requests
        fields = [
            'request_id',
            'employee_id',
            'approval_id',
            'material_id',
            'asset_id',
            'material_details',
            'asset_details',
            'purchase_description',
            'purchase_quantity',
            'valid_date',
            'document_date',
            'required_date',
        ]
    
    def validate(self, data):
        """
        Check that only one of material_id or asset_id is provided.
        """
        material_id = data.get('material_id')
        asset_id = data.get('asset_id')
        
        if material_id and asset_id:
            raise serializers.ValidationError(
                "Only one of material_id or asset_id should be provided, not both."
            )
            
        return data