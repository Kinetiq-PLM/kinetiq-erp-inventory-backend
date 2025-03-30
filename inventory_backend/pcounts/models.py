from django.db import models

# admin.products
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


class InventoryItem(models.Model):
    inventory_item_id = models.CharField(
        db_column='inventory_item_id',
        primary_key=True,
        max_length=255
    )

    product = models.ForeignKey(
        Products,
        to_field='item_id',       
        db_column='item_id',       
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    minimum_threshold = models.IntegerField(
        db_column='minimum_threshold',
        default=0
    )
    maximum_threshold = models.IntegerField(
        db_column='maximum_threshold',
        default=0
    )
    total_stock = models.IntegerField(
        db_column='total_stock',
        default=0
    )
    available_stock = models.IntegerField(
        db_column='available_stock',
        default=0
    )
    last_update = models.DateTimeField(
        db_column='last_update',
        auto_now_add=True
    )

    class Meta:
        managed = False
        db_table = 'inventory_item'

    def __str__(self):
        return self.product.product_name if self.product else "No Product"


class ProductData(models.Model):
    product_data_id = models.CharField(
        db_column='item_md_id',
        primary_key=True,
        max_length=50
    )
  
    inventory_item = models.ForeignKey(
        InventoryItem,
        db_column='inventory_item_id',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        managed = False
        db_table = 'inventory_product_data'

    def __str__(self):
        return self.product_data_id


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
    ('Verified', 'Verified'),
    ('Pending', 'Pending'),
    ('In-review', 'In-review'),
]


class CyclicCount(models.Model):
    inventory_count_id = models.CharField(
        db_column='inventory_count_id',
        primary_key=True,
        max_length=255
    )
    
    product_data = models.ForeignKey(
        ProductData,
        db_column='item_md_id',
        on_delete=models.CASCADE,
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
        return f"{self.inventory_count_id} - {self.status}"
