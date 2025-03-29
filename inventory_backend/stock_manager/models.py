from django.db import models

# 1. True Origin of Items – admin.item_master_data
class AdminItemMasterData(models.Model):
    item_id = models.CharField(
        db_column='item_id',
        primary_key=True,
        max_length=255
    )
    # Add any additional fields for the true item details here

    class Meta:
        managed = False
        db_table = 'item_master_data'

    def __str__(self):
        return self.item_id


# 2. Inventory Details – inventory.inventory_item_master_data
class InventoryItemMasterData(models.Model):
    item_md_id = models.CharField(
        db_column='item_md_id',
        primary_key=True,
        max_length=255
    )
    # Link to the true origin in admin.item_master_data via item_id
    admin_item = models.ForeignKey(
        AdminItemMasterData,
        db_column='item_id',
        to_field='item_id',
        on_delete=models.CASCADE
    )
    minimum_threshold = models.IntegerField(
        db_column='minimum_threshold',
        null=True,
        blank=True
    )
    maximum_threshold = models.IntegerField(
        db_column='maximum_threshold',
        null=True,
        blank=True
    )
    total_stock = models.IntegerField(
        db_column='total_stock',
        null=True,
        blank=True
    )
    stock_on_order = models.IntegerField(
        db_column='stock_on_order',
        null=True,
        blank=True
    )
    stock_committed = models.IntegerField(
        db_column='stock_committed',
        null=True,
        blank=True
    )
    available_stock = models.IntegerField(
        db_column='available_stock',
        null=True,
        blank=True
    )
    last_update = models.DateTimeField(
        db_column='last_update',
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'inventory_item_master_data'

    def __str__(self):
        return f"Inventory for {self.admin_item.item_id}"


# 3. Products – admin.products
class Products(models.Model):
    product_id = models.CharField(
        db_column='product_id',
        primary_key=True,
        max_length=255
    )
    item = models.ForeignKey(
        AdminItemMasterData,
        db_column='item_id',
        to_field='item_id',
        on_delete=models.CASCADE,  
        unique=True,
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


# 4. Assets – admin.assets - UPDATED with additional fields
class Assets(models.Model):
    asset_id = models.CharField(
        db_column='asset_id',
        primary_key=True,
        max_length=255
    )
    # Link to the true origin in AdminItemMasterData
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
    # Added fields from the database diagram
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


# 5. Raw Materials – admin.raw_materials - UPDATED with additional fields
class Raw_Materials(models.Model):
    material_id = models.CharField(
        db_column='material_id',
        primary_key=True,
        max_length=255
    )
    # Link to the true origin in AdminItemMasterData
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
    # Added fields from the database diagram
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