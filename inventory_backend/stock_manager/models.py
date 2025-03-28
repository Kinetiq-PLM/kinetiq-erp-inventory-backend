from django.db import models

class Assets(models.Model):
    asset_id = models.CharField(
        db_column='asset_id',
        primary_key=True,
        max_length=255
    )
    # Use the "item_id" column in ItemMasterData (which should be unique)
    item = models.ForeignKey(
        'ItemMasterData',
        to_field='item_id', 
        db_column='item_id',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    asset_name = models.CharField(
        db_column='asset_name',
        max_length=255,
    )

    class Meta:
        managed = False
        db_table = 'assets'

    def __str__(self):
        return self.asset_name


class Raw_materials(models.Model):
    material_id = models.CharField(
        db_column='material_id',  # Use material_id as the primary key column name
        primary_key=True,
        max_length=255
    )
    # Reference the unique "item_id" in ItemMasterData
    item = models.ForeignKey(
        'ItemMasterData',
        to_field='item_id',  
        db_column='item_id',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    material_name = models.CharField(
        db_column='material_name',
        max_length=255,
    )

    class Meta:
        managed = False
        db_table = 'raw_materials'

    def __str__(self):
        return self.material_name


# Master Product Data model (from admin.products)
class Products(models.Model):
    product_id = models.CharField(
        db_column='product_id',
        primary_key=True,
        max_length=255
    )
    item_id = models.CharField(
        db_column='item_id',
        max_length=255,
        null=True,
        blank=True,
        unique=True
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


# Item Master Data model 
class ItemMasterData(models.Model):
    item_md_id = models.CharField(
        db_column='item_md_id',
        primary_key=True,
        max_length=50
    )
    # Link to Products by matching its "item_id" field; this column will be named "item_id" in the database and must be unique
    item = models.ForeignKey(
        Products,
        to_field='item_id',
        db_column='item_id',
        null=True,
        blank=True,
        unique=True,
        on_delete=models.SET_NULL,
        related_name='item_master_data'
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
        product_name = self.item.product_name if self.item else 'Unknown Item'
        return f"{product_name} - Stock: {self.total_stock}"
