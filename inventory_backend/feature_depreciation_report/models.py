from django.db import models


class ExpiryReportData(models.Model):
    expiry_report_id = models.CharField(max_length=255, primary_key=True)
    item_name = models.CharField(max_length=255)
    item_type = models.CharField(max_length=50)
    item_management = models.CharField(max_length=50)
    item_no = models.CharField(max_length=255)
    expiry = models.DateTimeField()
    current_quantity = models.IntegerField()
    expiry_report_status = models.CharField(max_length=255)

    class Meta:
        managed = False  
        db_table = 'inventory"."vw_expiry_report_data' 
        
    def __str__(self):
        return self.item_name

class InventoryItemData(models.Model):
    inventory_item_id = models.CharField(max_length=255, primary_key=True)  
    item_type = models.CharField(max_length=50)
    item_name = models.CharField(max_length=255)
    item_management = models.CharField(max_length=50)
    item_no = models.CharField(max_length=255)
    current_quantity = models.IntegerField()
    shelf_life = models.CharField(max_length=50)
    expiry = models.DateTimeField()
    warehouse_id = models.CharField(max_length=255, null=True, blank=True)
    warehouse_location = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        managed = False  
        db_table = 'inventory"."vw_inventory_item_data' 
        
    def __str__(self):
        return self.item_name