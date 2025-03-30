        
from rest_framework import serializers
from .models import DeprecationReport

class DeprecationReportSerializer(serializers.ModelSerializer):
    content_id = serializers.CharField()  # Display content_id
    item_id = serializers.CharField()  # Display item_id
    quantity = serializers.IntegerField()
    status = serializers.CharField()
    warehouse = serializers.CharField()  # Display warehouse_id
    employee = serializers.CharField()  # Display employee_id

    class Meta:
        model = DeprecationReport
        fields = [
            'deprecation_report_id',
            'content_id',
            'item_id',
            'quantity',
            'status',
            'warehouse',
            'employee'
        ]