from rest_framework import serializers
from .models import CyclicCount, ProductData, InventoryItem, ItemMasterData, Product, Employee
import logging
import traceback
from django.db import connections

logger = logging.getLogger(__name__)

class CyclicCountSerializer(serializers.ModelSerializer):
    inventory_count_id = serializers.CharField(read_only=True)
    inventory_item_id = serializers.CharField(write_only=True, required=False)  
    employee_id = serializers.CharField(write_only=True, required=False)
    product_name = serializers.SerializerMethodField()
    item_id = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()
    debug_info = serializers.SerializerMethodField()

    class Meta:
        model = CyclicCount
        fields = [
            "inventory_count_id",
            "product_data_id",   
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
            "debug_info"
        ]

    def create(self, validated_data):
        if 'inventory_item_id' in validated_data:
            validated_data['product_data_id'] = validated_data.pop('inventory_item_id')
            
        if 'employee_id' in validated_data:
            employee_id = validated_data.pop('employee_id')
            try:
                employee = Employee.objects.get(employee_id=employee_id)
                validated_data['employee'] = employee
            except Employee.DoesNotExist:
                pass
                
        return super().create(validated_data)

    def get_product_name(self, obj):
        logger.info(f"Getting product_name for count_id: {obj.inventory_count_id}")
        
        # Get the inventory_item_id from the cyclic count record
        inventory_item_id = obj.product_data_id
        logger.info(f"Direct inventory_item_id from cyclic count: {inventory_item_id}")
        
        if not inventory_item_id:
            logger.error(f" Missing inventory_item_id for {obj.inventory_count_id}")
            return "No Inventory Item ID"
            
        # First try to find ProductData with this inventory_item_id
        direct_product_data = None
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute(
                    "SELECT item_md_id FROM inventory_product_data WHERE inventory_item_id = %s",
                    [inventory_item_id]
                )
                row = cursor.fetchone()
                if row:
                    logger.info(f"✓ Found product_data with item_md_id={row[0]} for inventory_item_id={inventory_item_id}")
                    try:
                        direct_product_data = ProductData.objects.get(product_data_id=row[0])
                    except ProductData.DoesNotExist:
                        logger.error(f" ProductData with ID {row[0]} exists in DB but not in ORM")
                else:
                    logger.error(f" No product_data found for inventory_item_id={inventory_item_id}")
        except Exception as e:
            logger.error(f"Error querying product_data: {str(e)}")
            
        # Try to fetch the full chain to get the product name
        try:
            # Get the inventory item
            inventory_item = InventoryItem.objects.filter(inventory_item_id=inventory_item_id).first()
            if not inventory_item:
                logger.error(f" No inventory_item found with ID={inventory_item_id}")
                return "No Inventory Item"
                
            logger.info(f"✓ Found inventory_item: {inventory_item.inventory_item_id}")
            
            # Get the item master data
            if not inventory_item.item:
                logger.error(f" Missing item master data for inventory_item {inventory_item.inventory_item_id}")
                return "No Item Master Data"
                
            logger.info(f"✓ Found item master data: {inventory_item.item.item_id}")
            
            # Get the product
            if not inventory_item.item.product:
                logger.error(f" Missing product for item {inventory_item.item.item_id}")
                return "No Product"
                
            product_name = inventory_item.item.product.product_name
            logger.info(f"✓ Found product_name: '{product_name}' for {obj.inventory_count_id}")
            return product_name
            
        except AttributeError as e:
            logger.error(f" AttributeError in relationship chain: {str(e)}")
            return f"Error: AttributeError - {str(e)}"
        except Exception as e:
            logger.error(f" Error getting product_name: {str(e)}")
            logger.error(traceback.format_exc())
            return f"Error: {str(e)}"

    def get_item_id(self, obj):
        try:
            inventory_item_id = obj.product_data_id
            if not inventory_item_id:
                return None
                
            inventory_item = InventoryItem.objects.filter(inventory_item_id=inventory_item_id).first()
            if not inventory_item or not inventory_item.item:
                return None
                
            return inventory_item.item.item_id
        except Exception as e:
            logger.error(f"Error getting item_id: {str(e)}")
            return None
            
    def get_employee(self, obj):
        try:
            if obj.employee:
                return obj.employee.employee_id
            return None
        except Exception as e:
            logger.error(f"Error getting employee: {str(e)}")
            return None
            
    def get_debug_info(self, obj):
        try:
            info = {
                "inventory_count_id": obj.inventory_count_id,
                "inventory_item_id": obj.product_data_id,
                "raw_db_data": {}
            }
            
            with connections['default'].cursor() as cursor:
               
                cursor.execute(
                    "SELECT inventory_item_id FROM inventory_cyclic_counts WHERE inventory_count_id = %s",
                    [obj.inventory_count_id]
                )
                row = cursor.fetchone()
                inventory_item_id = row[0] if row else None
                info["raw_db_data"]["inventory_item_id_in_cyclic_count"] = inventory_item_id
                
                if inventory_item_id:
                    # Check product_data
                    cursor.execute(
                        "SELECT item_md_id FROM inventory_product_data WHERE inventory_item_id = %s",
                        [inventory_item_id]
                    )
                    pd_row = cursor.fetchone()
                    info["raw_db_data"]["product_data_found"] = pd_row is not None
                    if pd_row:
                        info["raw_db_data"]["product_data_id"] = pd_row[0]
                        
                    # Check inventory_item
                    cursor.execute(
                        "SELECT item_id FROM inventory_item WHERE inventory_item_id = %s",
                        [inventory_item_id]
                    )
                    ii_row = cursor.fetchone()
                    info["raw_db_data"]["inventory_item_found"] = ii_row is not None
                    if ii_row:
                        info["raw_db_data"]["item_id"] = ii_row[0]
                        
                        # Check item master data
                        cursor.execute(
                            "SELECT product_id FROM item_master_data WHERE item_id = %s",
                            [ii_row[0]]
                        )
                        im_row = cursor.fetchone()
                        info["raw_db_data"]["item_master_data_found"] = im_row is not None
                        if im_row:
                            info["raw_db_data"]["product_id"] = im_row[0]
                            
                            # Check product
                            cursor.execute(
                                "SELECT product_name FROM products WHERE product_id = %s",
                                [im_row[0]]
                            )
                            p_row = cursor.fetchone()
                            info["raw_db_data"]["product_found"] = p_row is not None
                            if p_row:
                                info["raw_db_data"]["product_name"] = p_row[0]
            
            inventory_item = None
            try:
                inventory_item = InventoryItem.objects.get(inventory_item_id=inventory_item_id)
                info["orm_data"] = {
                    "inventory_item_found": True,
                    "inventory_item_id": inventory_item.inventory_item_id,
                    "has_item": inventory_item.item is not None
                }
                
                if inventory_item.item:
                    info["orm_data"]["item_id"] = inventory_item.item.item_id
                    info["orm_data"]["has_product"] = inventory_item.item.product is not None
                    
                    if inventory_item.item.product:
                        info["orm_data"]["product_id"] = inventory_item.item.product.product_id
                        info["orm_data"]["product_name"] = inventory_item.item.product.product_name
            except InventoryItem.DoesNotExist:
                info["orm_data"] = {"inventory_item_found": False}
            except Exception as e:
                info["orm_data"] = {"error": str(e)}
                
            return info
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }