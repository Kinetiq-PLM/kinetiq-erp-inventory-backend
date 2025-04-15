        
from rest_framework import serializers
from .models import ExpiryReport

class AssetsDeprecationReportSerializer(serializers.Serializer):
    deprecation_report_id = serializers.CharField()
    asset_id = serializers.CharField(source="inventory_item_id__asset_id")
    asset_name = serializers.CharField(source="inventory_item_id__asset_id__asset_name")
    status = serializers.CharField()
    reported_date = serializers.DateTimeField()
    quantity = serializers.IntegerField(source="inventory_item_id__current_quantity")
    

class RawMatDeprecationReportSerializer(serializers.Serializer):
    deprecation_report_id = serializers.CharField()
    material_id = serializers.CharField(source="inventory_item_id__material_id")
    material_name = serializers.CharField(source="inventory_item_id__material_id__material_name")
    status = serializers.CharField()
    reported_date = serializers.DateTimeField()
    quantity = serializers.IntegerField(source="inventory_item_id__current_quantity")

class ProductDeprecationReportSerializer(serializers.Serializer):
    deprecation_report_id = serializers.CharField()
    status = serializers.CharField()
    reported_date = serializers.DateTimeField()
    productdocu_id = serializers.CharField(source="inventory_item_id__productdocu_id")
    product_name = serializers.CharField(source="inventory_item_id__productdocu_id__product_id__product_name")
    expiry = serializers.DateField(source="inventory_item_id__expiry")
    quantity = serializers.IntegerField(source="inventory_item_id__current_quantity")

class ExpiryReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiryReport
        fields = ['expiry_report_id', 'expiry_report_status', 'item_management', 'item_identification', 'current_quantity', 'expiry', 'warehouse_id']