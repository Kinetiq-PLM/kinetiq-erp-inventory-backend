from django.db import models


# Dummy Model for Assets (to be replaced with actual model)
class Asset(models.Model):
    asset_id = models.CharField(
        db_column='asset_id',
        primary_key=True,
        max_length=255
    )

    asset_name = models.CharField(     
        db_column='asset_name',
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'admin"."assets'
        managed = False


class item_master_data(models.Model):
    item_id = models.CharField(
        db_column='item_id',
        primary_key=True,
        max_length=255
    )

    asset_id = models.ForeignKey(
        Asset,
        db_column='asset_id',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        db_table = 'admin"."item_master_data'  
        managed = False  
        

# Dummy Model for Raw Material (to be replaced with actual model)
class RawMaterial(models.Model):
    material_id = models.CharField(
        db_column='material_id',
        primary_key=True,
        max_length=255
    )

    material_name = models.CharField(
        db_column='material_name',
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'admin"."raw_materials'
        managed = False

class Product(models.Model):
    product_id = models.CharField(
        db_column='product_id',
        primary_key=True,
        max_length=255
    )

    product_name = models.CharField(
        db_column='product_name',
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'admin"."products'
        managed = False
        


# Dummy Model for Product Document (to be replaced with actual model)
class productDocument(models.Model):
    productdocu_id = models.CharField(
        db_column='productdocu_id',
        primary_key=True,
        max_length=255
    )

    product_id = models.ForeignKey(
        Product,
        db_column='product_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    expiry_date = models.DateField(
        db_column='expiry_date',
        auto_now_add=True,
        null=False,
    )


    class Meta:
        db_table = 'operations"."product_document_items'
        managed = False
          

# Dummy Model for FK: content_id (Document Item from Operations - to be replaced with actual model)
class DocumentItem(models.Model):
    content_id = models.CharField(
        db_column='content_id',
        primary_key=True,
        max_length=255
    )

    item_id = models.ForeignKey(
        item_master_data,
        db_column='item_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    material_id = models.ForeignKey(
        RawMaterial,
        db_column='material_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    productdocu_id = models.ForeignKey(
        productDocument,
        db_column='productdocu_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    quantity = models.IntegerField( 
        db_column='quantity',
        null=True,
        blank=True
    )


    class Meta:
        db_table = 'operations"."document_items'
        managed = False
        


class warehouse(models.Model):
    warehouse_id = models.CharField(
        db_column='warehouse_id',
        primary_key=True,
        max_length=255
    )

    warehouse_location = models.CharField(
        db_column='warehouse_location',
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'admin"."warehouse'
        managed = False

# Dummy Model for Employee (to be replaced with actual model) 
class Employee(models.Model):
    employee_id = models.CharField(
        db_column='employee_id',
        primary_key=True,
        max_length=50
    )
    first_name = models.CharField(
        db_column='first_name',
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'human_resources"."employees' 
        managed = False
         

class serial_tracking(models.Model):
    serial_id = models.CharField(
        db_column='serial_id',
        primary_key=True,
        max_length=255
    )

    item_id = models.ForeignKey(
        item_master_data,
        db_column='item_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    serial_no = models.CharField(
        db_column='serial_no',
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'operations"."serial_tracking'
        managed = False




class inventory_items(models.Model):
    inventory_item_id = models.CharField(
        db_column='inventory_item_id',
        primary_key=True,
        max_length=255
    )

    last_updated = models.DateTimeField(
        db_column='last_update',
        auto_now=True
    )

    serial_id = models.ForeignKey(
        serial_tracking,
        db_column='serial_id',
        on_delete=models.CASCADE,
        max_length=255,
        null=True,
        blank=True
    )

    productdocu_id = models.ForeignKey(
        productDocument,
        db_column='productdocu_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    material_id = models.ForeignKey(
        RawMaterial,
        db_column='material_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    asset_id = models.ForeignKey(
        Asset,
        db_column='asset_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    item_type = models.CharField(
        db_column='item_type',
        max_length=255,
        null=True,
        blank=True
    )

    current_quantity = models.IntegerField(
        db_column='current_quantity',
        null=True,
        blank=True
    )

    warehouse_id = models.ForeignKey(
        warehouse,
        db_column='warehouse_id',
        on_delete=models.CASCADE,   
        null=True,
        blank=True
    )

    date_created = models.DateTimeField(
        db_column='date_created',
        auto_now_add=True
    )

    expiry = models.DateField(
        db_column='expiry',
        null=False,
    )

    shelf_life = models.CharField(
        db_column='shelf_life',
        max_length=20,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'inventory"."inventory_item'  # <- add this!
        managed = False







#  ----- Configurations for Main Model: Depreciation Report -----

class ExpiryReport(models.Model):
    fields = (
        'expiry_report_id',
        'expiry_report_status',
        'item_management',
        'item_identification',
        'current_quantity',
        'expiry',
        'warehouse_id',
    )


    class Meta:
        db_table = 'inventory"."vw_expiry_report' 
        managed = False
      
    def __str__(self):
      return f"{self.expiry_report_id} - {self.status}"
    
class InventoryItemData(models.Model):
    inventory_item_id = models.CharField(max_length=255, primary_key=True)  
    item_type = models.CharField(max_length=50)
    item_name = models.CharField(max_length=255)
    item_management = models.CharField(max_length=50)
    item_management_id = models.CharField(max_length=255)
    current_quantity = models.IntegerField()
    shelf_life = models.CharField(max_length=50)
    expiry = models.DateField(null=True, blank=True)  
    warehouse_location = models.CharField(max_length=255, null=True, blank=True)
    
    
    class Meta:
        managed = False  
        db_table = 'inventory"."vw_inventory_item_data' 
        
    def __str__(self):
        return self.item_name