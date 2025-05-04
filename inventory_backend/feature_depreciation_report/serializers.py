        
from rest_framework import serializers
from .models import ExpiryReportData

class ExpiryReportDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiryReportData
        fields = ['expiry_report_id',
                  'item_name',
                  'item_type',
                  'item_management', 'item_no',
                  'expiry',
                  'current_quantity',
                  'expiry_report_status',]

        