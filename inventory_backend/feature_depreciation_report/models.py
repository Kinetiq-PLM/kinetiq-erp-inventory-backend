from django.db import models

# Create your models here.

class Warehouse(models.Model):
    """
    Model to represent the warehouse.
    """
    warehouse_id = models.CharField(
        db_column='warehouse_id',
        primary_key=True,
        max_length=255
    )

    warehouse_name = models.CharField(
        db_column='warehouse_name',
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        managed = False  # This table already exists
        db_table = 'warehouses'


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
    
class content(models.Model):
    """
    Model to represent the content of the warehouse.
    """
    content_id = models.CharField(
        db_column='content_id',
        primary_key=True,
        max_length=255
    )

    class Meta:
        managed = False  # This table already exists
        db_table = 'content'


# Main Model for Depreciation Report
class DepreciationReport(models.Model):
    """
    Model to represent the depreciation report.
    """
    depreciation_report_id = models.CharField(
        db_column='depreciation_report_id',
        primary_key=True,
        max_length=255
    )

    content_id = models.ForeignKey(
        content,
        db_column='content_id',
        on_delete=models.CASCADE, 
        null=True,
        blank=True
    )

    item_id = models.CharField(
        db_column='item_id',
        max_length=255,
        null=True,
        blank=True,
        unique=True
    )

    quantity = models.IntegerField(
        db_column='quantity',
        null=True,
        blank=True
    )
   
    status = models.enums.CharField(
        db_column='status',
        max_length=20,
        choices=[
            ('in_transit', 'In Transit'),
            ('completed', 'Completed'),
        ]
    )
  
    warehouse = models.ForeignKey(
        Warehouse,
        db_column='warehouse_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    employee = models.ForeignKey(
        Employee,
        db_column='employee_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    


    class Meta:
        managed = False  # This table already exists
        db_table = 'depreciation_report'



