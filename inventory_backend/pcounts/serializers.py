from rest_framework import serializers
from .models import CyclicCount

class CyclicCountSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    item_id = serializers.SerializerMethodField()  # from Products

    class Meta:
        model = CyclicCount
        fields = [
            "inventory_count_id",
            "item_md",
            "item_id",
            "product_name",
            "item_onhand",
            "item_actually_counted",
            "difference_in_qty",
            "employee",
            "status",
            "remarks",
            "time_period"
        ]

    def get_product_name(self, obj):
        try:
            return obj.item_md.item.product_name if obj.item_md and obj.item_md.item else None
        except AttributeError:
            return None

    def get_item_id(self, obj):
        try:
            return obj.item_md.item.item_id if obj.item_md and obj.item_md.item else None
        except AttributeError:
            return None
