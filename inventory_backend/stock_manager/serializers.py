from rest_framework import serializers
from .models import (
    ItemMasterData, InventoryItem, InventoryItemThreshold,
    Purchase_requests, QuotationContent, PurchaseQuotation,
    ProductInventoryView, AssetInventoryView, RawMaterialInventoryView,
    WarehouseProductStockView, WarehouseAssetStockView, WarehouseMaterialStockView,
    WarehouseAllItemStockView
)
import logging

logger = logging.getLogger(__name__)

class AdminItemMasterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemMasterData
        fields = [
            'item_id',
            'item_name',
            'item_type',
            'unit_of_measure',
            'item_status'
        ]


class InventoryItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.item_name', read_only=True)
    item_id_display = serializers.CharField(source='item.item_id', read_only=True)

    class Meta:
        model = InventoryItem
        fields = [
            'inventory_item_id',
            'item',
            'item_id_display',
            'item_name',
            'item_no',
            'item_type',
            'current_quantity',
            'warehouse_id',
            'expiry',
            'shelf_life',
            'start_of_depreciation',
            'is_active',
            'is_demo_item',
            'last_update',
            'date_created'
        ]
        read_only_fields = ['last_update', 'date_created']
        extra_kwargs = {
            'item': {'write_only': True, 'required': True, 'allow_null': False}
        }

    def create(self, validated_data):
        item_id = validated_data.pop('item', None)
        if item_id:
            try:
                item_instance = ItemMasterData.objects.get(pk=item_id)
                validated_data['item'] = item_instance
            except ItemMasterData.DoesNotExist:
                raise serializers.ValidationError(f"ItemMasterData with id {item_id} does not exist.")
            except TypeError:
                if isinstance(item_id, ItemMasterData):
                    validated_data['item'] = item_id
                else:
                    raise serializers.ValidationError("Invalid value provided for 'item'. Expected item_id.")
        return super().create(validated_data)


class InventoryItemThresholdSerializer(serializers.ModelSerializer):
    item_id = serializers.CharField(source='item.item_id', read_only=True)
    item_name = serializers.CharField(source='item.item_name', read_only=True)

    class Meta:
        model = InventoryItemThreshold
        fields = [
            'inventory_item_threshold_id',
            'item',
            'item_id',
            'item_name',
            'minimum_threshold',
            'maximum_threshold'
        ]
        extra_kwargs = {
            'item': {'write_only': True, 'required': True, 'allow_null': False}
        }

    def create(self, validated_data):
        item_id = validated_data.pop('item', None)
        if item_id:
            try:
                item_instance = ItemMasterData.objects.get(pk=item_id)
                validated_data['item'] = item_instance
            except ItemMasterData.DoesNotExist:
                raise serializers.ValidationError(f"ItemMasterData with id {item_id} does not exist.")
            except TypeError:
                if isinstance(item_id, ItemMasterData):
                    validated_data['item'] = item_id
                else:
                    raise serializers.ValidationError("Invalid value provided for 'item'. Expected item_id.")
        return super().create(validated_data)


class PurchaseRequestSerializer(serializers.ModelSerializer):
    request_id = serializers.CharField(read_only=True)

    class Meta:
        model = Purchase_requests
        fields = [
            'request_id',
            'employee_id',
            'valid_date',
            'document_date',
            'required_date',
            'status'
        ]


class QuotationContentSerializer(serializers.ModelSerializer):
    quotation_content_id = serializers.CharField(read_only=True)
    item_details = AdminItemMasterDataSerializer(source='item', read_only=True)

    class Meta:
        model = QuotationContent
        fields = [
            'quotation_content_id',
            'request',
            'item',
            'item_details',
            'purchase_quantity',
            'unit_price',
            'discount',
            'tax_code',
            'total',
        ]
        extra_kwargs = {
            'request': {'write_only': True, 'required': True, 'allow_null': False},
            'item': {'write_only': True, 'required': True, 'allow_null': False}
        }

    def validate(self, data):
        return data

    def create(self, validated_data):
        item_id = validated_data.pop('item', None)
        request_id = validated_data.pop('request', None)

        if item_id:
            try:
                item_instance = ItemMasterData.objects.get(pk=item_id)
                validated_data['item'] = item_instance
            except ItemMasterData.DoesNotExist:
                raise serializers.ValidationError({"item": f"ItemMasterData with id {item_id} does not exist."})
            except TypeError:
                if not isinstance(item_id, ItemMasterData):
                    raise serializers.ValidationError({"item": "Invalid value provided for 'item'. Expected item_id."})
                else:
                    validated_data['item'] = item_id

        if request_id:
            try:
                request_instance = Purchase_requests.objects.get(pk=request_id)
                validated_data['request'] = request_instance
            except Purchase_requests.DoesNotExist:
                raise serializers.ValidationError({"request": f"Purchase Request with id {request_id} does not exist."})
            except TypeError:
                if not isinstance(request_id, Purchase_requests):
                    raise serializers.ValidationError({"request": "Invalid value provided for 'request'. Expected request_id."})
                else:
                    validated_data['request'] = request_id

        return super().create(validated_data)


class PurchaseQuotationSerializer(serializers.ModelSerializer):
    request_details = PurchaseRequestSerializer(source='request', read_only=True)

    class Meta:
        model = PurchaseQuotation
        fields = [
            'quotation_id',
            'request',
            'request_details',
            'vendor_code',
            'document_no',
            'valid_date',
            'document_date',
            'required_date',
            'buyer',
            'remarks',
            'delivery_loc',
            'downpayment_request',
            'total_before_discount',
            'discount_percent',
            'freight',
            'tax',
            'total_payment',
            'owner',
            'status',
        ]
        read_only_fields = ['quotation_id']
        extra_kwargs = {
            'request': {'write_only': True, 'required': True, 'allow_null': False}
        }

    def create(self, validated_data):
        request_id = validated_data.pop('request', None)
        if request_id:
            try:
                request_instance = Purchase_requests.objects.get(pk=request_id)
                validated_data['request'] = request_instance
            except Purchase_requests.DoesNotExist:
                raise serializers.ValidationError({"request": f"Purchase Request with id {request_id} does not exist."})
            except TypeError:
                if not isinstance(request_id, Purchase_requests):
                    raise serializers.ValidationError({"request": "Invalid value provided for 'request'. Expected request_id."})
                else:
                    validated_data['request'] = request_id
        return super().create(validated_data)


class ProductInventoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventoryView
        fields = [
            'item_id',
            'item_name',
            'stock_committed',
            'total_stock',
            'available_stock',
            'minimum_threshold',
            'maximum_threshold',
            'last_update'
        ]


class AssetInventoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetInventoryView
        fields = [
            'item_id',
            'item_name',
            'stock_on_order',
            'total_stock',
            'minimum_threshold',
            'maximum_threshold',
            'last_update'
        ]


class RawMaterialInventoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialInventoryView
        fields = [
            'item_id',
            'item_name',
            'stock_on_order',
            'total_stock',
            'minimum_threshold',
            'maximum_threshold',
            'last_update'
        ]


# --- WAREHOUSE SPECIFIC VIEW SERIALIZERS ---

class WarehouseProductStockViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProductStockView
        fields = [
            'id', # Optional, might not be needed by frontend if filtering by item/whs
            'item_id',
            'item_name',
            'warehouse_id',
            'total_stock',
            'stock_committed', # Currently placeholder
            'available_stock', # Currently placeholder (total)
            'minimum_threshold',
            'maximum_threshold',
            'last_update'
        ]

class WarehouseAssetStockViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseAssetStockView
        fields = [
            'id', # Optional
            'item_id',
            'item_name',
            'warehouse_id',
            'total_stock',
            'stock_on_order', # Currently placeholder
            'minimum_threshold',
            'maximum_threshold',
            'last_update'
        ]

class WarehouseMaterialStockViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseMaterialStockView
        fields = [
            'id', # Optional
            'item_id',
            'item_name',
            'warehouse_id',
            'total_stock',
            'stock_on_order', # Currently placeholder
            'minimum_threshold',
            'maximum_threshold',
            'last_update'
        ]

# --- COMBINED WAREHOUSE STOCK VIEW SERIALIZER ---

class WarehouseAllItemStockViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseAllItemStockView
        fields = [
            'id', # Optional
            'item_id',
            'item_name',
            'warehouse_id',
            'item_type',
            'total_stock',
            'stock_committed',
            'available_stock',
            'stock_on_order',
            'minimum_threshold',
            'maximum_threshold',
            'last_update'
        ]
