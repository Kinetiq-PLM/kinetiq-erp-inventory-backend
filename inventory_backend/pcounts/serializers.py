from rest_framework import serializers
from .models import CyclicCount, InventoryItemThreshold, InventoryItem, ItemMasterData, Product
import logging
import traceback
from django.db import connections
from django.db import connection
from django.apps import apps

# print("!!!!!!!! SERIALIZERS.PY FILE LOADED !!!!!!!") # Removed diagnostic print

logger = logging.getLogger(__name__)

class CyclicCountSerializer(serializers.ModelSerializer):
    # print("---- CyclicCountSerializer CLASS DEFINITION EXECUTED ----") # Removed diagnostic print

    # Field for writing/linking the inventory_item relationship
    inventory_item_id = serializers.PrimaryKeyRelatedField(
        queryset=InventoryItem.objects.all(), 
        source='inventory_item', 
        write_only=True, 
        required=True
    )
    # Read-only representation of the inventory_item ID
    item_display_name = serializers.SerializerMethodField() 
    
    employee = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()
    warehouse_location = serializers.SerializerMethodField()
    uom = serializers.SerializerMethodField()

    class Meta:
        model = CyclicCount
        fields = [
            "inventory_count_id",       # Read-only (PK)
            "inventory_item_id",        # Write-only (custom field above, maps to 'inventory_item' model field)
            "item_display_name",        # Read-only (method field)
            "item_onhand",              # Read/Write (model field)
            "item_actually_counted",    # Read/Write (model field)
            "difference_in_qty",        # Read/Write (model field)
            
            "employee_id",              # For writing the model's employee_id field
            "employee",                 # Read-only (method field for display)
            
            "status",                   # Read/Write (model field)
            "remarks",                  # Read/Write (model field)
            "time_period",              # Read/Write (model field)
            
            "warehouse_id",             # For writing the model's warehouse_id field
            "warehouse_location",       # Read-only (method field for display)
            
            "item_type",                # Read-only (method field)
            "uom",                      # Read-only (method field)
        ]
        extra_kwargs = {
            'inventory_count_id': {'read_only': True},
            'employee_id': {
                'write_only': True, 
                'required': True # Match frontend validation
            },
            'warehouse_id': {
                'write_only': True, 
                'required': True # Match frontend validation
            },
            # The following read_only_fields are now implicitly handled by SerializerMethodField 
            # or by 'write_only' on the direct model fields above.
            # 'item_display_name': {'read_only': True},
            # 'employee': {'read_only': True},
            # 'item_type': {'read_only': True},
            # 'warehouse_location': {'read_only': True},
            # 'uom': {'read_only': True},
        }
        # No longer need a separate read_only_fields list here if using write_only and SerializerMethodFields effectively
        # read_only_fields = [
        #     "inventory_count_id",
        #     "item_display_name", 
        #     "employee", 
        #     "item_type",
        #     "warehouse_location", 
        #     "uom",
        # ]

    def to_representation(self, instance):
        # print(f"---- Serializing CyclicCount ID: {instance.inventory_count_id} ----") # Removed diagnostic print
        representation = super().to_representation(instance)
        return representation

    def create(self, validated_data):
        inventory_item_instance = validated_data.pop('inventory_item', None)
        employee_id_val = validated_data.get('employee_id')
        # print(f"Creating count with employee_id: {employee_id_val}, warehouse_id: {validated_data.get('warehouse_id')}") # Removed diagnostic print

        if 'item_actually_counted' in validated_data and 'item_onhand' in validated_data:
             validated_data['difference_in_qty'] = validated_data['item_actually_counted'] - validated_data['item_onhand']
        elif 'difference_in_qty' not in validated_data: 
             validated_data['difference_in_qty'] = 0 

        instance = CyclicCount.objects.create(inventory_item=inventory_item_instance, **validated_data)
        return instance

    def get_item_type(self, obj):
        try:
            if obj.inventory_item: 
                return obj.inventory_item.item_type
            return "Unknown"
        except AttributeError:
             logger.warning(f"Inventory item not found for CyclicCount {obj.inventory_count_id}")
             return "Unknown"
        except Exception as e:
            logger.error(f"Error getting item_type for {obj.inventory_count_id}: {str(e)}")
            return "Unknown"
            
    def get_item_display_name(self, obj):
        display_name = "N/A"
        try:
            related_inventory_item = obj.inventory_item 
            if not related_inventory_item:
                logger.warning(f"CyclicCount {obj.inventory_count_id}: No related InventoryItem found.")
                return obj.inventory_item_id or display_name

            # logger.debug(f"CyclicCount {obj.inventory_count_id}: Found InventoryItem {related_inventory_item.inventory_item_id}") # Removed

            master_item_id = related_inventory_item.item_id
            if master_item_id:
                # logger.debug(f"Attempting ItemMasterData lookup with item_id: {master_item_id}") # Removed
                try:
                    item_master = ItemMasterData.objects.get(item_id=master_item_id)
                    if item_master.item_name and item_master.item_name.strip():
                        display_name = item_master.item_name.strip()
                        # logger.debug(f"Found name in ItemMasterData: {display_name}") # Removed
                        return display_name 
                    else:
                        logger.warning(f"ItemMasterData found for {master_item_id}, but item_name is empty.")
                except ItemMasterData.DoesNotExist:
                    logger.warning(f"ItemMasterData not found for item_id: {master_item_id}")
                except Exception as e:
                     logger.error(f"Error fetching ItemMasterData for {master_item_id}: {str(e)}")
            else:
                logger.warning(f"InventoryItem {related_inventory_item.inventory_item_id} has no master item_id to look up.")

            item_number = related_inventory_item.item_no
            if item_number and item_number.strip():
                display_name = item_number.strip()
                # logger.debug(f"Using fallback InventoryItem.item_no: {display_name}") # Removed
                return display_name

            if master_item_id and master_item_id.strip():
                display_name = master_item_id.strip()
                # logger.debug(f"Using fallback InventoryItem.item_id: {display_name}") # Removed
                return display_name

            display_name = obj.inventory_item_id or "N/A"
            # logger.debug(f"Using final fallback CyclicCount.inventory_item_id: {display_name}") # Removed
            return display_name

        except AttributeError as e:
             logger.error(f"AttributeError in get_item_display_name for {obj.inventory_count_id}: {str(e)}.")
             return obj.inventory_item_id or "N/A"
        except Exception as e:
            logger.error(f"Generic error in get_item_display_name for {obj.inventory_count_id}: {str(e)}")
            return obj.inventory_item_id or "N/A"

    def get_employee(self, obj):
        emp_id = obj.employee_id
        if not emp_id:
            return "Unassigned"
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    ''' 
                    SELECT first_name, last_name 
                    FROM admin.users 
                    WHERE employee_id = %s 
                    ''',
                    [emp_id]
                )
                result = cursor.fetchone()
            
            if result and result[0] and result[1]:
                return f"{result[0]} {result[1]}"
            else:
                logger.warning(f"User not found in admin.users for employee_id: {emp_id}")
                return emp_id # Fallback to ID
        except Exception as e:
            logger.error(f"Error fetching employee name for employee_id {emp_id}: {str(e)}")
            return emp_id # Fallback to ID

    def get_warehouse_location(self, obj):
        try:
            if obj.warehouse_id:
                with connection.cursor() as cursor:
                    cursor.execute(
                        ''' 
                        SELECT warehouse_location 
                        FROM admin.warehouse 
                        WHERE warehouse_id = %s
                        ''', 
                        [obj.warehouse_id]
                    )
                    result = cursor.fetchone()
                if result and result[0]:
                    return result[0] 
            return None 
        except Exception as e:
            logger.error(f"Error getting warehouse_location for {obj.inventory_count_id}: {str(e)}")
            return None 

    def get_uom(self, obj):
        try:
            related_inventory_item = obj.inventory_item
            if not related_inventory_item:
                return "N/A"

            master_item_id = related_inventory_item.item_id
            if master_item_id:
                try:
                    item_master = ItemMasterData.objects.get(item_id=master_item_id)
                    # Ensure unit_of_measure exists and is not empty
                    if item_master.unit_of_measure and item_master.unit_of_measure.strip():
                        return item_master.unit_of_measure.strip()
                    else:
                        logger.warning(f"ItemMasterData {master_item_id} found, but unit_of_measure is empty.")
                except ItemMasterData.DoesNotExist:
                    # If master data doesn't exist, we can't get UOM from it
                    logger.warning(f"ItemMasterData not found for item_id: {master_item_id} to get UOM.")
                except Exception as e:
                     logger.error(f"Error fetching UOM from ItemMasterData for {master_item_id}: {str(e)}")
            else:
                # If inventory item doesn't link to master data
                logger.warning(f"InventoryItem {related_inventory_item.inventory_item_id} has no master item_id to get UOM.")

            # Fallback if UOM couldn't be found via ItemMasterData
            return "N/A"

        except Exception as e:
            logger.error(f"Generic error in get_uom for {obj.inventory_count_id}: {str(e)}")
            return "N/A"

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
    Includes fields matching the updated model and SQL schema.
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
            'item_id',
            'item_no',
            'start_of_depreciation',
            'is_active',
            'is_demo_item'
        ]

class InventoryItemThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItemThreshold
        fields = '__all__'

