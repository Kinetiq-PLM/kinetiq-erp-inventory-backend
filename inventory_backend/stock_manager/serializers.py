from rest_framework import serializers
from .models import (
    Product, ItemMasterData, InventoryItemData, InventoryItemThreshold,
    Asset, RawMaterial, Purchase_requests, QuotationContent, PurchaseQuotation,
    ProductInventoryView, AssetInventoryView, RawMaterialInventoryView
)
import logging

logger = logging.getLogger(__name__)

class AdminItemMasterDataSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)

    class Meta:
        model = ItemMasterData
        fields = [
            'item_id',
            'product_name'
        ]


class InventoryItemDataSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.material_name', read_only=True)
    asset_name = serializers.CharField(source='asset.asset_name', read_only=True)

    class Meta:
        model = InventoryItemData
        fields = [
            'inventory_item_id',
            'serial_id',
            'productdocu_id',
            'material',
            'material_name',
            'asset',
            'asset_name',
            'item_type',
            'current_quantity',
            'warehouse_id',
            'date_created'
        ]


class InventoryItemThresholdSerializer(serializers.ModelSerializer):
    item_id = serializers.CharField(source='item.item_id', read_only=True)

    class Meta:
        model = InventoryItemThreshold
        fields = [
            'inventory_item_threshold_id',
            'item_id',
            'minimum_threshold',
            'maximum_threshold'
        ]


class ProductsSerializer(serializers.ModelSerializer):
    item_id = serializers.SerializerMethodField()
    admin_item = serializers.SerializerMethodField()
    inventory_data = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'product_id',
            'product_name',
            'description',
            'selling_price',
            'stock_level',
            'warranty_period',
            'policy_id',
            'batch_no',
            'item_status',
            'content_id',
            'unit_of_measure',
            'item_id',
            'admin_item',
            'inventory_data'
        ]

    def get_admin_item(self, obj):
    
        item = obj.itemmasterdata_set.first()
        if item:
            return AdminItemMasterDataSerializer(item).data
        return None

    def get_item_id(self, obj):
        item = obj.itemmasterdata_set.first()
        if item:
            return item.item_id
        return None

    def get_inventory_data(self, obj):
        try:
            item = obj.itemmasterdata_set.first()
            if not item:
                return {}
                
            # Get threshold data
            threshold = InventoryItemThreshold.objects.filter(item=item).first()
            threshold_data = {}
            if threshold:
                threshold_data = {
                    'minimum_threshold': threshold.minimum_threshold,
                    'maximum_threshold': threshold.maximum_threshold
                }
            
            # Get inventory items related to this product
            inventory_items = InventoryItemData.objects.filter(material__product_id=obj.product_id)
            
            # Calculate total quantity
            total_quantity = sum(item.current_quantity for item in inventory_items)
            
            data = {
                'item_id': item.item_id,
                'current_quantity': total_quantity,
                **threshold_data
            }
            
            return data
        except Exception as e:
            logger.error(f"Error merging inventory data for product {obj.product_id}: {str(e)}")
            return {}


class AssetsSerializer(serializers.ModelSerializer):

    item_id = serializers.SerializerMethodField()
    admin_item = serializers.SerializerMethodField()
    inventory_data = serializers.SerializerMethodField()
    purchase_date = serializers.DateField(format="%Y-%m-%d", required=False)
    serial_no = serializers.CharField(required=False)

    class Meta:
        model = Asset
        fields = [
            'asset_id', 
            'admin_item',
            'item_id', 
            'asset_name', 
            'purchase_date',
            'serial_no',
            'inventory_data'
        ]

    def get_admin_item(self, obj):
        item = obj.itemmasterdata_set.first()
        if item:
            return AdminItemMasterDataSerializer(item).data
        return None

    def get_item_id(self, obj):
        item = obj.itemmasterdata_set.first()
        if item:
            return item.item_id
        return None

    def get_inventory_data(self, obj):
        item = obj.itemmasterdata_set.first()
        if not item:
            return {}
        try:
            # Get threshold data
            threshold = InventoryItemThreshold.objects.filter(item=item).first()
            threshold_data = {}
            if threshold:
                threshold_data = {
                    'minimum_threshold': threshold.minimum_threshold,
                    'maximum_threshold': threshold.maximum_threshold
                }
            
            # Get inventory items related to this asset
            inventory_items = InventoryItemData.objects.filter(asset=obj)
            
            # Calculate total quantity
            total_quantity = sum(item.current_quantity for item in inventory_items)
            
            return {
                'item_id': item.item_id,
                'current_quantity': total_quantity,
                **threshold_data,
                'last_update': inventory_items[0].date_created if inventory_items else None
            }
        except Exception as e:
            logger.error(f"Error getting inventory data for asset {obj.asset_id}: {str(e)}")
            return {}


class RawMaterialsSerializer(serializers.ModelSerializer):

    item_id = serializers.SerializerMethodField()
    admin_item = serializers.SerializerMethodField()
    inventory_data = serializers.SerializerMethodField()
    description = serializers.CharField(required=False)
    unit_of_measure = serializers.CharField(required=False)

    class Meta:
        model = RawMaterial
        fields = [
            'material_id', 
            'admin_item',
            'item_id', 
            'material_name',
            'description',
            'unit_of_measure',
            'inventory_data'
        ]

    def get_admin_item(self, obj):
        item = obj.itemmasterdata_set.first()
        if item:
            return AdminItemMasterDataSerializer(item).data
        return None

    def get_item_id(self, obj):
        item = obj.itemmasterdata_set.first()
        if item:
            return item.item_id
        return None

    def get_inventory_data(self, obj):
        item = obj.itemmasterdata_set.first()
        if not item:
            return {}
        try:
            # Get threshold data
            threshold = InventoryItemThreshold.objects.filter(item=item).first()
            threshold_data = {}
            if threshold:
                threshold_data = {
                    'minimum_threshold': threshold.minimum_threshold,
                    'maximum_threshold': threshold.maximum_threshold
                }
            
            # Get inventory items related to this material
            inventory_items = InventoryItemData.objects.filter(material=obj)
            
            # Calculate total quantity
            total_quantity = sum(item.current_quantity for item in inventory_items)
            
            return {
                'item_id': item.item_id,
                'current_quantity': total_quantity,
                **threshold_data,
                'last_update': inventory_items[0].date_created if inventory_items else None
            }
        except Exception as e:
            logger.error(f"Error getting inventory data for material {obj.material_id}: {str(e)}")
            return {}


class PurchaseRequestSerializer(serializers.ModelSerializer):
    request_id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Purchase_requests
        fields = [
            'request_id',
            'employee_id',
            'approval_id',
            'valid_date',
            'document_date',
            'required_date',
        ]
        
    def create(self, validated_data):
        """
        Create a new purchase request with an auto-generated request_id.
        """
        # The database trigger will generate the request_id
        instance = Purchase_requests.objects.create(**validated_data)
        return instance

class QuotationContentSerializer(serializers.ModelSerializer):
    quotation_content_id = serializers.CharField(read_only=True)
    material_details = RawMaterialsSerializer(source='material', read_only=True)
    asset_details = AssetsSerializer(source='asset', read_only=True)
    request_details = PurchaseRequestSerializer(source='request', read_only=True)
    
    class Meta:
        model = QuotationContent
        fields = [
            'quotation_content_id',
            'request',
            'request_details',
            'unit_price',
            'discount',
            'tax_code',
            'total',
            'material',
            'asset',
            'material_details',
            'asset_details',
            'purchase_quantity',
        ]
    
    def validate(self, data):
        """
        Check that only one of material or asset is provided.
        """
        material = data.get('material')
        asset = data.get('asset')
        
        if material and asset:
            raise serializers.ValidationError(
                "Only one of material or asset should be provided, not both."
            )
            
        return data
        
    def create(self, validated_data):
        """
        Create a new quotation content with an auto-generated quotation_content_id.
        """
        # The database trigger will generate the quotation_content_id
        instance = QuotationContent.objects.create(**validated_data)
        return instance

class PurchaseQuotationSerializer(serializers.ModelSerializer):
    request_details = PurchaseRequestSerializer(source='request', read_only=True)
    
    class Meta:
        model = PurchaseQuotation
        fields = [
            'quotation_id',
            'vendor_id',
            'request',
            'request_details',
        ]

class ProductInventoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventoryView
        fields = ['product_id', 'stock_committed', 'total_stock', 'available_stock', 
                 'minimum_threshold', 'maximum_threshold', 'last_update']

class AssetInventoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetInventoryView
        fields = ['asset_id', 'stock_on_order', 'total_stock', 
                 'minimum_threshold', 'maximum_threshold', 'last_update']

class RawMaterialInventoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialInventoryView
        fields = ['material_id', 'stock_on_order', 'total_stock', 
                 'minimum_threshold', 'maximum_threshold', 'last_update']
