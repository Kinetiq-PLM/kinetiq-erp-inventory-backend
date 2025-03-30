        
from rest_framework import serializers
from .models import DeprecationReport, DocumentItem,  Asset, RawMaterial, productDocument, Employee

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterial
        fields = '__all__'

class productDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = productDocument
        fields = '__all__'

class DocumentItemSerializer(serializers.ModelSerializer):
    asset_id = AssetSerializer(read_only=True)
    material_id = RawMaterialSerializer(read_only=True)  
    productdocu_id = productDocumentSerializer(read_only=True) 

    class Meta:
        model = DocumentItem
        fields = '__all__'

class DeprecationReportSerializer(serializers.ModelSerializer):
    content_id = DocumentItemSerializer(read_only=True)
    employee = serializers.CharField(source='employee.first_name', read_only=True) # Assuming Employee model has first_name field

    class Meta:
        model = DeprecationReport
        fields = '__all__'