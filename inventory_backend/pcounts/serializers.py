from rest_framework import serializers
from .models import CyclicCount, ProductData, InventoryItem, ItemMasterData, Product, Employee
import logging

logger = logging.getLogger(__name__)

class CyclicCountSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    item_id = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()
    debug_info = serializers.SerializerMethodField()

    class Meta:
        model = CyclicCount
        fields = [
            "inventory_count_id",
            "product_data",
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

    def get_product_name(self, obj):
        try:
            if not obj.product_data:
                logger.info(f"No product_data for {obj.inventory_count_id}")
                return "No Product Data"
            if not obj.product_data.inventory_item:
                logger.info(f"No inventory_item for {obj.inventory_count_id}")
                return "No Inventory Item"
            if not obj.product_data.inventory_item.item:
                logger.info(f"No item master data for {obj.inventory_count_id}")
                return "No Item Master Data"
            if not obj.product_data.inventory_item.item.product:
                logger.info(f"No product for {obj.inventory_count_id}")
                return "No Product"
            product_name = obj.product_data.inventory_item.item.product.product_name
            logger.info(f"Found product_name: {product_name} for {obj.inventory_count_id}")
            return product_name
        except Exception as e:
            logger.error(f"Error getting product_name for {obj.inventory_count_id}: {str(e)}")
            return f"Error: {str(e)}"

    def get_item_id(self, obj):
        try:
            if obj.product_data and obj.product_data.inventory_item and obj.product_data.inventory_item.item:
                return obj.product_data.inventory_item.item.item_id
            return None
        except Exception as e:
            logger.error(f"Error getting item_id: {str(e)}")
            return None
            
    def get_employee(self, obj):
        try:
            if obj.employee:
                return f"{obj.employee.first_name} {obj.employee.last_name}"
            return None
        except Exception as e:
            logger.error(f"Error getting employee: {str(e)}")
            return None
            
    def get_debug_info(self, obj):
        try:
            info = {
                "has_product_data": obj.product_data is not None,
            }
            if obj.product_data:
                info["product_data_id"] = obj.product_data.product_data_id
                info["has_inventory_item"] = obj.product_data.inventory_item is not None
                if obj.product_data.inventory_item:
                    info["inventory_item_id"] = obj.product_data.inventory_item.inventory_item_id
                    info["has_item_master"] = obj.product_data.inventory_item.item is not None
                    if obj.product_data.inventory_item.item:
                        info["item_id"] = obj.product_data.inventory_item.item.item_id
                        info["has_product"] = obj.product_data.inventory_item.item.product is not None
                        if obj.product_data.inventory_item.item.product:
                            info["product_id"] = obj.product_data.inventory_item.item.product.product_id
                            info["product_name"] = obj.product_data.inventory_item.item.product.product_name
            return info
        except Exception as e:
            return {"error": str(e)}