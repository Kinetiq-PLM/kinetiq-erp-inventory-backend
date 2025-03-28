from rest_framework import serializers
from .models import Products, ItemMasterData, Assets, Raw_materials

class ItemMasterDataSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='item.product_name', read_only=True)

    class Meta:
        model = ItemMasterData
        fields = [
            'item_md_id', 
            'item', 
            'product_name',
            'minimum_threshold', 
            'maximum_threshold', 
            'total_stock', 
            'stock_on_order', 
            'stock_committed', 
            'available_stock', 
            'last_update'
        ]

class ProductsSerializer(serializers.ModelSerializer):
    item_master_data = ItemMasterDataSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = [
            'product_id', 
            'item_id', 
            'product_name', 
            'item_master_data'
        ]

class AssetsSerializer(serializers.ModelSerializer):
    available_stock = serializers.SerializerMethodField()

    class Meta:
        model = Assets
        fields = ['asset_id', 'item', 'asset_name', 'available_stock']

    def get_available_stock(self, obj):
        if obj.item:
            return obj.item.available_stock
        return None


class RawMaterialsSerializer(serializers.ModelSerializer):
    available_stock = serializers.SerializerMethodField()

    class Meta:
        model = Raw_materials
        fields = ['material_id', 'item', 'material_name', 'available_stock']

    def get_available_stock(self, obj):
        if obj.item:
            return obj.item.available_stock
        return None
