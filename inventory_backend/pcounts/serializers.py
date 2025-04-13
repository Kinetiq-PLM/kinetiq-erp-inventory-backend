from rest_framework import serializers
from .models import CyclicCount, InventoryItemThreshold, InventoryItem, ItemMasterData, Product, Employee
import logging
import traceback
from django.db import connections

logger = logging.getLogger(__name__)

class CyclicCountSerializer(serializers.ModelSerializer):
    inventory_count_id = serializers.CharField(read_only=True)
    inventory_item_id = serializers.CharField(write_only=True, required=True)
    employee_id = serializers.CharField(write_only=True, required=False)
    product_name = serializers.SerializerMethodField()
    item_id = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField(method_name='get_employee_id')
    warehouse_id_input = serializers.CharField(write_only=True, required=False)
    item_type = serializers.SerializerMethodField()

    class Meta:
        model = CyclicCount
        fields = [
            "inventory_count_id",
            "inventory_item_id",
            "employee_id",
            "item_onhand",
            "item_actually_counted",
            "difference_in_qty",
            "employee",
            "status",
            "remarks",
            "time_period",
            "item_id",
            "product_name",
            "warehouse_id",
            "warehouse_id_input",
            "item_type",
        ]
        read_only_fields = [
            "product_name",
            "item_id",
            "employee",
            "item_type",
        ]

    def get_item_type(self, obj):
        try:
            if obj.inventory_item:
                return obj.inventory_item.item_type
            return "Unknown"
        except Exception as e:
            logger.error(f"Error getting item_type: {str(e)}")
            return "Unknown"

    def create(self, validated_data):
        inventory_item_id = validated_data.pop('inventory_item_id', None)
        if inventory_item_id:
            try:
                inventory_item = InventoryItem.objects.get(inventory_item_id=inventory_item_id)
                validated_data['inventory_item'] = inventory_item
                
                # If warehouse_id_input was provided, use it for the cyclic count's warehouse_id
                warehouse_id = validated_data.pop('warehouse_id_input', None)
                if warehouse_id:
                    validated_data['warehouse_id'] = warehouse_id
                # If not provided but inventory item has warehouse_id, use that
                elif inventory_item.warehouse_id:
                    validated_data['warehouse_id'] = inventory_item.warehouse_id
            except InventoryItem.DoesNotExist:
                raise serializers.ValidationError({"inventory_item_id": f"InventoryItem with id {inventory_item_id} does not exist."})
        else:
            raise serializers.ValidationError({"inventory_item_id": "This field is required."})

        employee_id_str = validated_data.pop('employee_id', None)
        if employee_id_str:
            try:
                employee_instance = Employee.objects.get(employee_id=employee_id_str)
                validated_data['employee'] = employee_instance
            except Employee.DoesNotExist:
                raise serializers.ValidationError({"employee_id": f"Employee with id {employee_id_str} does not exist."})

        instance = super().create(validated_data)
        return instance

    def get_product_name(self, obj):
        try:
            if obj.inventory_item:
                item_type = obj.inventory_item.item_type
                if item_type == "Product":
                    product_id = obj.inventory_item.productdocu_id
                    if product_id:
                        try:
                            product = Product.objects.get(product_id=product_id)
                            return product.product_name
                        except Product.DoesNotExist:
                            return f"Product {product_id} not found"
                    return f"Item is Product type: {obj.inventory_item.inventory_item_id}"
                return f"Item type: {item_type}"
            else:
                return "No Inventory Item"
        except AttributeError as e:
            logger.error(f"AttributeError getting product_name: {str(e)}")
            return "Error: Attribute Error"
        except Exception as e:
            logger.error(f"Error getting product_name: {str(e)}")
            logger.error(traceback.format_exc())
            return f"Error: {str(e)}"

    def get_item_id(self, obj):
        try:
            if obj.inventory_item:
                if hasattr(obj.inventory_item, 'productdocu_id') and obj.inventory_item.productdocu_id:
                    return obj.inventory_item.productdocu_id
                elif hasattr(obj.inventory_item, 'material_id') and obj.inventory_item.material_id:
                    return obj.inventory_item.material_id
                elif hasattr(obj.inventory_item, 'asset_id') and obj.inventory_item.asset_id:
                    return obj.inventory_item.asset_id
                return obj.inventory_item.inventory_item_id
            return None
        except Exception as e:
            logger.error(f"Error getting item_id: {str(e)}")
            return None
            
    def get_employee_id(self, obj):
        try:
            if obj.employee:
                return obj.employee.employee_id
            return None
        except Exception as e:
            logger.error(f"Error getting employee_id: {str(e)}")
            return None
            
    def get_warehouse_id(self, obj):
        try:
            if obj.inventory_item and hasattr(obj.inventory_item, 'warehouse_id'):
                return obj.inventory_item.warehouse_id
            return None
        except Exception as e:
            logger.error(f"Error getting warehouse_id: {str(e)}")
            return None

# Add the missing serializers
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ItemMasterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemMasterData
        fields = '__all__'

class InventoryItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the InventoryItem model.
    Explicitly includes all fields needed by the frontend, with special attention to item_type.
    """
    class Meta:
        model = InventoryItem
        fields = [
            'inventory_item_id',
            'item_type',
            'current_quantity',
            'warehouse_id',
            'expiry',
            'shelf_life',
            'last_update',
            'date_created',
            'serial_id',
            'productdocu_id',
            'material_id',
            'asset_id'
        ]

class InventoryItemThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItemThreshold
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
