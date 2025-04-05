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
         


#  ----- Configurations for Main Model: Depreciation Report -----

# Status Choices for Report Items
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
]

# Main Model for Depreciation Report
class DeprecationReport(models.Model):
    deprecation_report_id = models.CharField(
        db_column='deprecation_report_id',
        primary_key=True,
        max_length=255
    )
    
    content_id = models.ForeignKey(
        DocumentItem,
        db_column='content_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    reported_date = models.DateTimeField(
        db_column='reported_date',
        auto_now_add=True
    )

    status = models.CharField(
        db_column='status',
        max_length=20,
        choices=STATUS_CHOICES,
    )

    
    Employee = models.ForeignKey(
        Employee,
        db_column='employee_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'inventory"."deprecation_report'
        managed = False
      

    def __str__(self):
      return f"{self.depreciation_report_id} - {self.status}"