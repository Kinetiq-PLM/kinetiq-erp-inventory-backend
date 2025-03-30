        
from rest_framework import serializers
from .models import DeprecationReport, DocumentItem,  Asset, RawMaterial, productDocument, Employee

class DeprecationReportSerializer(serializers.Serializer):
    deprecation_report_id = serializers.CharField()
    status = serializers.CharField()
    reported_date = serializers.DateTimeField()
    content_id = serializers.CharField()  
    asset_id = serializers.CharField(source="content_id__asset_id")
    asset_name = serializers.CharField(source="content_id__asset_id__asset_name")
    material_id = serializers.CharField(source="content_id__material_id")
    material_name = serializers.CharField(source="content_id__material_id__material_name")
    productdocu_id = serializers.CharField(source="content_id__asset_id")
    productdocu_id = serializers.CharField(source="content_id__productdocu_id")
    expiry_date = serializers.DateField(source="content_id__productdocu_id__expiry_date")
