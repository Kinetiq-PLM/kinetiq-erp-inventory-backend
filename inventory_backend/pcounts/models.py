from django.db import models

class Product(models.Model):
    product_id = models.CharField(
        db_column='product_id',
        primary_key=True,
        max_length=255
    )
    product_name = models.CharField(
        db_column='product_name',
        max_length=255
    )
    description = models.TextField(
        db_column='description',
        null=True,
        blank=True
    )
    selling_price = models.DecimalField(
        db_column='selling_price',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    class Meta:
        managed = False
        db_table = 'products'
        app_label = 'pcounts' 

    def __str__(self):
        return self.product_name


class ItemMasterData(models.Model):
    item_id = models.CharField(
        db_column='item_id',
        primary_key=True,
        max_length=255
    )
    item_name = models.CharField(
        db_column='item_name',
        max_length=255,
        null=False
    )
    item_type = models.CharField(
        db_column='item_type',
        max_length=50,
        null=True
    )
    unit_of_measure = models.CharField(
        db_column='unit_of_measure',
        max_length=50,
        null=True
    )
    manage_item_by = models.CharField(
        db_column='manage_item_by',
        max_length=50,
        null=True
    )
    item_status = models.CharField(
        db_column='item_status',
        max_length=50,
        null=True
    )
    preferred_vendor = models.CharField(
        db_column='preferred_vendor',
        max_length=255,
        null=True
    )
    purchasing_uom = models.CharField(
        db_column='purchasing_uom',
        max_length=50,
        null=True
    )
    items_per_purchase_unit = models.IntegerField(
        db_column='items_per_purchase_unit',
        null=True
    )
    purchase_quantity_per_package = models.IntegerField(
        db_column='purchase_quantity_per_package',
        null=True
    )
    sales_uom = models.CharField(
        db_column='sales_uom',
        max_length=50,
        null=True
    )
    items_per_sale_unit = models.IntegerField(
        db_column='items_per_sale_unit',
        null=True
    )
    sales_quantity_per_package = models.IntegerField(
        db_column='sales_quantity_per_package',
        null=True
    )
    item_description = models.TextField(
        db_column='item_description',
        null=True
    )

    class Meta:
        managed = False
        db_table = 'admin"."item_master_data'

    def __str__(self):
        return self.item_name if self.item_name else self.item_id


class InventoryItem(models.Model):
    SHELF_LIFE_CHOICES = [
        ('Depreciating', 'Depreciating'),
        ('Expiring', 'Expiring'),
    ]
    
    ITEM_TYPE_CHOICES = [
        ('Product', 'Product'),
        ('Asset', 'Asset'),
        ('Material', 'Material'),
    ]
    
    inventory_item_id = models.CharField(
        db_column='inventory_item_id',
        primary_key=True,
        max_length=255
    )
    item_id = models.CharField(
        db_column='item_id',
        max_length=255,
        null=True,
        blank=True
    )
    item_no = models.CharField(
        db_column='item_no',
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    start_of_depreciation = models.DateTimeField(
        db_column='start_of_depreciation',
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        db_column='is_active',
        default=True,
    )
    is_demo_item = models.BooleanField(
        db_column='is_demo_item',
        default=False,
    )
    item_type = models.CharField(
        db_column='item_type',
        max_length=50,
        choices=ITEM_TYPE_CHOICES
    )
    current_quantity = models.IntegerField(
        db_column='current_quantity'
    )
    warehouse_id = models.CharField(
        db_column='warehouse_id',
        max_length=255,
        null=True,
        blank=True
    )
    expiry = models.DateTimeField(
        db_column='expiry',
        null=True,
        blank=True
    )
    shelf_life = models.CharField(
        db_column='shelf_life',
        max_length=20,
        choices=SHELF_LIFE_CHOICES,
        null=True,
        blank=True
    )
    last_update = models.DateTimeField(
        db_column='last_update',
    )
    date_created = models.DateTimeField(
        db_column='date_created',
    )

    class Meta:
        managed = False
        db_table = 'inventory"."inventory_item'

    def __str__(self):
        return self.item_id or self.item_no or self.inventory_item_id


class InventoryItemThreshold(models.Model):
    inventory_item_threshold_id = models.CharField(
        db_column='inventory_item_threshold_id',
        primary_key=True,
        max_length=50
    )
    item = models.ForeignKey(
        ItemMasterData,
        db_column='item_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    minimum_threshold = models.IntegerField(
        db_column='minimum_threshold'
    )
    maximum_threshold = models.IntegerField(
        db_column='maximum_threshold'
    )

    class Meta:
        managed = False
        db_table = 'inventory"."inventory_item_threshold'

    def __str__(self):
        return f"Threshold for {self.item_id if self.item_id else 'unknown item'}"


class CyclicCount(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Closed', 'Closed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    TIME_PERIOD_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    inventory_count_id = models.CharField(
        db_column='inventory_count_id',
        primary_key=True,
        max_length=255
    )
    inventory_item = models.ForeignKey(
        InventoryItem,
        db_column='inventory_item_id',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    item_onhand = models.IntegerField(
        db_column='item_onhand'
    )
    item_actually_counted = models.IntegerField(
        db_column='item_actually_counted'
    )
    difference_in_qty = models.IntegerField(
        db_column='difference_in_qty'
    )
    employee_id = models.CharField(
        db_column='employee_id',
        max_length=255,
        null=True,
        blank=True
    )
    status = models.CharField(
        db_column='status',
        max_length=20,
        choices=STATUS_CHOICES
    )
    remarks = models.TextField(
        db_column='remarks',
        null=True,
        blank=True
    )
    time_period = models.CharField(
        db_column='time_period',
        max_length=20,
        choices=TIME_PERIOD_CHOICES
    )
    warehouse_id = models.CharField(
        db_column='warehouse_id',
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'inventory"."inventory_cyclic_counts'

    def __str__(self):
        return f"Count {self.inventory_count_id}"