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

    def __str__(self):
        return self.item_id



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


class Warehouse(models.Model):
    warehouse_id = models.CharField(max_length=255, primary_key=True)
    warehouse_location = models.CharField(max_length=255, null=True, blank=True)  

    class Meta:
        db_table = 'admin"."warehouse'  

    def __str__(self):
        return self.warehouse_id


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

    batch_no = models.CharField(
        db_column='batch_no',
        max_length=255,
        null=True,
        blank=True
    )

    serial_id = models.CharField(
        db_column='serial_id',
        max_length=255,
        null=True,
        blank=True
    )

    quantity = models.IntegerField( 
        db_column='quantity',
        null=True,
        blank=True
    )

    warehouse_id = models.ForeignKey(
        Warehouse,
        db_column='warehouse_id',
        on_delete=models.CASCADE,
        max_length=255,
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




# Bridge Models (placeholders for foreign key relationships)


class PurchaseOrder(models.Model):
    purchase_id = models.CharField(max_length=255, primary_key=True)

    class Meta:
        db_table = 'purchasing"."purchase_order'  
        managed = False

    def __str__(self):
        return self.purchase_id

class Order(models.Model):
    order_id = models.CharField(max_length=255, primary_key=True)

    class Meta:
        db_table = 'sales"."order'
        managed = False

    def __str__(self):
        return self.order_id



# Main Model for warehouse_movement
class WarehouseMovement(models.Model):
    movement_id = models.CharField(max_length=255, primary_key=True)
    item = models.ForeignKey(
        item_master_data,
        on_delete=models.CASCADE,
        db_column='item_id'
    )
    movement_type = models.CharField(max_length=255)  
    quantity = models.IntegerField()
    movement_date = models.DateTimeField()
    destination = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        db_column='destination',
        related_name='destination_movements'
    )
    source = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        db_column='source',
        related_name='source_movements'
    )
    reference_id_purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        db_column='reference_id_purchase_order',
        null=True,
        blank=True
    )
    reference_id_order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        db_column='reference_id_order',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'inventory"."warehouse_movement'  
        managed = False  

    def __str__(self):
        return f"{self.movement_id} - {self.movement_type}"