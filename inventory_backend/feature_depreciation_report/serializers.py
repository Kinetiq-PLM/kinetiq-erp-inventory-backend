# # inventory/serializers.py
# from rest_framework import serializers
# from .models import WarehouseMovement, Warehouse

# class WarehouseMovementSerializer(serializers.ModelSerializer):
#     item = serializers.CharField(source='item.item_id')  # Display item_id
#     destination = serializers.CharField(source='destination.warehouse_id')  # Display warehouse_id
#     source = serializers.CharField(source='source.warehouse_id')  # Display warehouse_id
#     reference_id_purchase_order = serializers.CharField(
#         source='reference_id_purchase_order.purchase_id', allow_null=True
#     )
#     reference_id_order = serializers.CharField(
#         source='reference_id_order.order_id', allow_null=True
#     )

#     class Meta:
#         model = WarehouseMovement
#         fields = [
#             'movement_id',
#             'item',
#             'movement_type',
#             'quantity',
#             'movement_date',
#             'destination',
#             'source',
#             'reference_id_purchase_order',
#             'reference_id_order',
#         ]

# class WarehouseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Warehouse
#         fields = ['warehouse_id', 'warehouse_location']  

        
from rest_framework import serializers
from .models import DepreciationReport, Warehouse, Employee, content

class DepreciationReportSerializer(serializers.ModelSerializer):
    content_id = serializers.CharField(source='content.content_id')  # Display content_id
    item_id = serializers.CharField(source='item.item_id')  # Display item_id
    quantity = serializers.IntegerField()
    status = serializers.CharField()
    warehouse = serializers.CharField(source='warehouse.warehouse_id')  # Display warehouse_id
    employee = serializers.CharField(source='employee.employee_id')  # Display employee_id

    class Meta:
        model = DepreciationReport
        fields = [
            'depreciation_report_id',
            'content_id',
            'item_id',
            'quantity',
            'status',
            'warehouse',
            'employee'
        ]