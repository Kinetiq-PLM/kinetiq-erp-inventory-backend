from rest_framework import serializers
from .models import Products, AdminItemMasterData, InventoryItemMasterData, Assets, Raw_Materials, Purchase_requests

class AdminItemMasterDataSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)

    class Meta:
        model = AdminItemMasterData
        fields = [
            'item_id',
            'product_name'
        ]

class InventoryItemMasterDataSerializer(serializers.ModelSerializer):
    admin_item = AdminItemMasterDataSerializer(read_only=True)

    class Meta:
        model = InventoryItemMasterData
        fields = [
            'item_md_id',
            'admin_item',
            'minimum_threshold',
            'maximum_threshold',
            'total_stock',
            'stock_on_order',
            'stock_committed',
            'available_stock',
            'last_update'
        ]

class ProductsSerializer(serializers.ModelSerializer):
    item_id = serializers.CharField(source='item.item_id', read_only=True)
    admin_item = AdminItemMasterDataSerializer(source='item', read_only=True)

    class Meta:
        model = Products
        fields = [
            'product_id',
            'item',  
            'item_id',
            'product_name',
            'admin_item'
        ]

class AssetsSerializer(serializers.ModelSerializer):
    available_stock = serializers.SerializerMethodField()
    item_id = serializers.CharField(source='item.item_id', read_only=True)
    
    # Added fields for assets
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
            'available_stock'
        ]

    def get_available_stock(self, obj):
        if obj.item:
            try:
                inventory = InventoryItemMasterData.objects.get(admin_item=obj.item)
                return inventory.available_stock
            except InventoryItemMasterData.DoesNotExist:
                return None
        return None

class RawMaterialsSerializer(serializers.ModelSerializer):
    available_stock = serializers.SerializerMethodField()
    item_id = serializers.CharField(source='item.item_id', read_only=True)
    
    # Added fields for raw materials
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
            'available_stock'
        ]

    def get_available_stock(self, obj):
        if obj.item:
            try:
                inventory = InventoryItemMasterData.objects.get(admin_item=obj.item)
                return inventory.available_stock
            except InventoryItemMasterData.DoesNotExist:
                return None
        return None
    
from rest_framework import serializers
from .models import Purchase_requests, Assets, Raw_Materials

class PurchaseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase_requests
        fields = '__all__'
    
    def validate_item_id(self, value):
        asset_exists = Assets.objects.filter(asset_id=value).exists()
        material_exists = Raw_Materials.objects.filter(material_id=value).exists()
        
        if not (asset_exists or material_exists):
            raise serializers.ValidationError(
                "Item ID must be a valid Asset ID or Material ID."
            )
        return value