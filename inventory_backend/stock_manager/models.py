from django.db import models

# 1. True Origin of Items 
class AdminItemMasterData(models.Model):
    item_id = models.CharField(
        db_column='item_id',
        primary_key=True,
        max_length=255
    )

    class Meta:
        managed = False
        db_table = 'item_master_data'

    def __str__(self):
        return self.item_id


# 2. Inventory Item Data 
class InventoryItemData(models.Model):
    inventory_item_id = models.CharField(
        db_column='inventory_item_id',  
        primary_key=True,
        max_length=255
    )
    admin_item = models.OneToOneField(
        AdminItemMasterData,
        db_column='item_id',  
        to_field='item_id',
        on_delete=models.CASCADE,
        related_name='inventory_item'
    )
    minimum_threshold = models.IntegerField(
        db_column='minimum_threshold',
        null=True,
        blank=True,
        default=0
    )
    maximum_threshold = models.IntegerField(
        db_column='maximum_threshold',
        null=True,
        blank=True,
        default=0
    )
    total_stock = models.IntegerField(
        db_column='total_stock',
        null=True,
        blank=True,
        default=0
    )
    available_stock = models.IntegerField(
        db_column='available_stock',
        null=True,
        blank=True,
        default=0
    )
    last_update = models.DateTimeField(
        db_column='last_update',
        null=True,
        blank=True
    )

    class Meta:
        managed = False 
        db_table = 'inventory_item'

    def __str__(self):
        return f"ItemData for {self.admin_item.item_id}"


# 3. Inventory Product Data 
class InventoryProductData(models.Model):
    item_md_id = models.CharField(
        db_column='item_md_id',
        primary_key=True,
        max_length=255
    )
    inventory_item = models.ForeignKey(
        InventoryItemData,
        db_column='inventory_item_id',  
        to_field='inventory_item_id',  
        on_delete=models.CASCADE,
        related_name='product_data' 
    )
    stock_on_order = models.IntegerField(
        db_column='stock_on_order',
        null=True,
        blank=True,
        default=0
    )
    stock_committed = models.IntegerField(
        db_column='stock_committed',
        null=True,
        blank=True,
        default=0
    )

    class Meta:
        managed = False
        db_table = 'inventory_product_data'  


# 4. Products
class Products(models.Model):
    product_id = models.CharField(
        db_column='product_id',
        primary_key=True,
        max_length=255
    )
    item = models.OneToOneField(
        AdminItemMasterData,
        db_column='item_id',
        to_field='item_id',
        on_delete=models.CASCADE,
        related_name='product'
    )
    product_name = models.CharField(
        db_column='product_name',
        max_length=255
    )

    class Meta:
        managed = False
        db_table = 'products'

    def __str__(self):
        return self.product_name

# 5. Assets 
class Assets(models.Model):
    asset_id = models.CharField(
        db_column='asset_id',
        primary_key=True,
        max_length=255
    )
    item = models.ForeignKey(
        AdminItemMasterData,
        db_column='item_id',
        to_field='item_id',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    asset_name = models.CharField(
        db_column='asset_name',
        max_length=255
    )
    purchase_date = models.DateField(
        db_column='purchase_date',
        null=True,
        blank=True
    )
    serial_no = models.CharField(  
        db_column='serial_no',
        max_length=50,  
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'assets'

    def __str__(self):
        return self.asset_name


# 6. Raw Materials 
class Raw_Materials(models.Model):
    material_id = models.CharField(
        db_column='material_id',
        primary_key=True,
        max_length=255
    )
    item = models.ForeignKey(
        AdminItemMasterData,
        db_column='item_id',
        to_field='item_id',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    material_name = models.CharField(
        db_column='material_name',
        max_length=255
    )
    description = models.TextField(
        db_column='description',
        null=True,
        blank=True
    )
    unit_of_measure = models.CharField(
        db_column='unit_of_measure',
        max_length=50,
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'raw_materials'

    def __str__(self):
        return self.material_name


# 7. Purchase Requests
class Purchase_requests(models.Model):
    request_id = models.CharField(
        primary_key=True,
        max_length=255
    )
    employee_id = models.CharField(  
        max_length=255,
        null=True,
        blank=True
    )
    approval_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    item_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    purchase_item = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    purchase_description = models.TextField(
        null=True,
        blank=True
    )
    purchase_quantity = models.IntegerField(
        null=True,
        blank=True
    )
    valid_date = models.DateField(
        null=True,
        blank=True
    )
    document_date = models.DateField(
        null=True,
        blank=True
    )
    required_date = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'purchase_requests'

    def __str__(self):
        return self.item_id