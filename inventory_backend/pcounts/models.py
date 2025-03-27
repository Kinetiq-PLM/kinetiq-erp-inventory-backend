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
        managed = False  # This table already exists
        db_table = 'products'

    def __str__(self):
        return self.product_name


# Item Master Data model (bridge table)
class ItemMasterData(models.Model):
    item_md_id = models.CharField(
        db_column='item_md_id',
        primary_key=True,
        max_length=50
    )
    item = models.ForeignKey(
        Products,
        to_field='item_id',  # Link using item_id (not product_id)
        db_column='item_id',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        managed = False
        db_table = 'inventory_item_master_data'


# Minimal Employee model representing human_resources.employees
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

# Cyclic Count model
class CyclicCount(models.Model):
    inventory_count_id = models.CharField(
        db_column='inventory_count_id',
        primary_key=True,
        max_length=255
    )

    item_md = models.ForeignKey(
        ItemMasterData,
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
