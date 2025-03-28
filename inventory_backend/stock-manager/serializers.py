from rest_framework import serializers
from .models import Products, ItemMasterData, Employee, CyclicCount

class ItemMasterDataSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='item.product_name', read_only=True)

    class Meta:
        model = ItemMasterData
        fields = [
            'item_md_id', 
            'item', 
            'product_name',
            'unit_cost', 
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