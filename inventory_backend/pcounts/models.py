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
    asset_id = models.CharField(
        db_column='asset_id',
        max_length=255,
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        'Product',
        db_column='product_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    material_id = models.CharField(
        db_column='material_id',
        max_length=255,
        null=True,
        blank=True
    )
    item_type = models.CharField(
        db_column='item_type',
        max_length=50,
        null=True,
        blank=True
    )
    item_name = models.CharField(
        db_column='item_name',
        max_length=255,
        null=True,
        blank=True
    )
    unit_of_measure = models.CharField(
        db_column='unit_of_measure',
        max_length=50,
        null=True,
        blank=True
    )
    manage_item_by = models.CharField(
        db_column='manage_item_by',
        max_length=100,
        null=True,
        blank=True
    )
    item_status = models.CharField(
        db_column='item_status',
        max_length=50,
        null=True,
        blank=True
    )
    preferred_vendor = models.CharField(
        db_column='preferred_vendor',
        max_length=255,
        null=True,
        blank=True
    )
    purchasing_uom = models.CharField(
        db_column='purchasing_uom',
        max_length=50,
        null=True,
        blank=True
    )
    items_per_purchase_unit = models.IntegerField(
        db_column='items_per_purchase_unit',
        null=True,
        blank=True
    )
    purchase_quantity_per_package = models.IntegerField(
        db_column='purchase_quantity_per_package',
        null=True,
        blank=True
    )
    sales_uom = models.CharField(
        db_column='sales_uom',
        max_length=50,
        null=True,
        blank=True
    )
    items_per_sale_unit = models.IntegerField(
        db_column='items_per_sale_unit',
        null=True,
        blank=True
    )
    sales_quantity_per_package = models.IntegerField(
        db_column='sales_quantity_per_package',
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'item_master_data'

    def __str__(self):
        return self.item_name if self.item_name else self.item_id


class InventoryItem(models.Model):
    inventory_item_id = models.CharField(
        db_column='inventory_item_id',
        primary_key=True,
        max_length=255
    )
    serial_id = models.CharField(
        db_column='serial_id',
        max_length=255,
        null=True,
        blank=True
    )
    productdocu_id = models.CharField(
        db_column='productdocu_id',
        max_length=255,
        null=True,
        blank=True
    )
    material_id = models.CharField(
        db_column='material_id',
        max_length=255,
        null=True,
        blank=True
    )
    asset_id = models.CharField(
        db_column='asset_id',
        max_length=255,
        null=True,
        blank=True
    )
    item_type = models.CharField(
        db_column='item_type',
        max_length=50
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
    date_created = models.DateTimeField(
        db_column='date_created',
        editable=False
    )

    class Meta:
        managed = False
        db_table = 'inventory_item'

    def __str__(self):
        return self.inventory_item_id


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
        db_table = 'inventory_item_threshold'

    def __str__(self):
        if self.item:
            return f"Thresholds for {self.item.item_id} ({self.item.item_name or 'No Name'})"
        return self.inventory_item_threshold_id


class Employee(models.Model):
    employee_id = models.CharField(
        db_column='employee_id',
        primary_key=True,
        max_length=50
    )
    first_name = models.CharField(
        db_column='first_name',
        max_length=100
    )
    last_name = models.CharField(
        db_column='last_name',
        max_length=100
    )

    class Meta:
        managed = False
        db_table = 'employees'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


STATUS_CHOICES = [
    ('Completed', 'Completed'),
    ('In Progress', 'In Progress'),
    ('Open', 'Open'),
    ('Closed', 'Closed'),
]


class CyclicCount(models.Model):
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
        db_column='item_onhand',
        null=True,
        blank=True
    )
    item_actually_counted = models.IntegerField(
        db_column='item_actually_counted',
        null=True,
        blank=True
    )
    difference_in_qty = models.IntegerField(
        db_column='difference_in_qty',
        null=True,
        blank=True
    )
    employee = models.ForeignKey(
        Employee,
        db_column='employee_id',
        on_delete=models.SET_NULL,
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
        max_length=50,
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'inventory_cyclic_counts'

    def __str__(self):
        item_name = self.inventory_item.inventory_item_id if self.inventory_item else "No Item"
        return f"{self.inventory_count_id} - {item_name} - {self.status}"