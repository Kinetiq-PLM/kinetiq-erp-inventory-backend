from django.db import models

# Create your models here.

# Dummy model to represent the warehouse.


#  dummy model to represent the Employee.

STATUS_CHOICES = [
    ('in_transit', 'In Transit'),
    ('completed', 'Completed'),
]

# Main Model for Depreciation Report
class DeprecationReport(models.Model):
    """
    Model to represent the deprication report.
    """
    deprecation_report_id = models.CharField(
        db_column='deprecation_report_id',
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

    content_id = models.CharField(
        db_column='content_id',
        max_length=255,
        null=True,
        blank=True
    )



    quantity = models.IntegerField(
        db_column='quantity',
        null=True,
        blank=True
    )
   
    status = models.CharField(
        db_column='status',
        max_length=20,
        choices=STATUS_CHOICES,
    )
  
    warehouse = models.CharField(
        db_column='warehouse_id',
        null=True,
        blank=True
    )

    employee = models.CharField(
        db_column='employee_id',
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'inventory"."deprecation_report'  # Correct format for PostgreSQL


    def __str__(self):
      return f"{self.depreciation_report_id} - {self.status}"



# class Meta:
#         db_table = 'inventory"."warehouse_movement'  
#         managed = False  
# inventory.deprecation_report