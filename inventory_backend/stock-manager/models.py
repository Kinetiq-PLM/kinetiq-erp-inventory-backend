from django.db import models

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
    item = models.ForeignKey(
        Products,
        to_field='item_id',
        db_column='item_id',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='item_master_data' 
    )

    unit_cost = models.DecimalField(
        db_column='unit_cost',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
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
        db_table = 'item_master_data'

    def __str__(self):
        return f"{self.item.product_name if self.item else 'Unknown Item'} - Stock: {self.total_stock}"


