from django.db import models

class Warehouse(models.Model):
    warehouse_id = models.CharField(max_length=255, primary_key=True)
    warehouse_location = models.CharField(max_length=255, null=True, blank=True)  

    class Meta:
        db_table = 'admin"."warehouse'  

    def __str__(self):
        return self.warehouse_id


class InventoryItemData(models.Model):
    inventory_item_id = models.CharField(max_length=255, primary_key=True)  
    item_type = models.CharField(max_length=50)
    item_name = models.CharField(max_length=255)
    item_management = models.CharField(max_length=50)
    item_management_id = models.CharField(max_length=255)
    current_quantity = models.IntegerField()
    shelf_life = models.CharField(max_length=50)
    expiry = models.DateTimeField()
    warehouse_id = models.CharField(max_length=255, null=True, blank=True)
    warehouse_location = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        managed = False  
        db_table = 'inventory"."vw_inventory_item_data' 
        
    def __str__(self):
        return self.item_name

class InventoryItem(models.Model):
    inventory_item_id = models.CharField(max_length=255, primary_key=True)  
    class Meta:
        managed = False  
        db_table = 'inventory"."inventory_item' 
        
    def __str__(self):
        return self.inventory_item_id

class WarehouseMovement(models.Model):

    class MovementStatus(models.TextChoices):
        OPEN = 'Open', 'Open'
        IN_PROGRESS = 'In Progress', 'In Progress'
        COMPLETED = 'Completed', 'Completed'
        CLOSED = 'Closed', 'Closed'
        CANCELLED = 'Cancelled', 'Cancelled'


    movement_id = models.CharField(primary_key=True, max_length=255, editable=False)
    docu_creation_date = models.DateTimeField()
    movement_date = models.DateTimeField()
    movement_status = models.CharField(
    max_length=20,
    choices=MovementStatus.choices,
    default=MovementStatus.COMPLETED
    )
    destination = models.CharField(max_length=255)
    source = models.CharField(max_length=255, null=True)
    # reference_id_purchase_order = models.CharField(max_length=255, null=True)
    # reference_id_order = models.CharField(max_length=255, null=True, blank=True)
    comments = models.CharField(max_length=255, null= True, blank=True)

    class Meta:
        managed = False
        db_table = 'inventory"."warehouse_movement'

    def __str__(self):
        return self.movement_id


class WarehouseMovementItem(models.Model):
    warehouse_movement_items_id = models.CharField(max_length=255, unique=True, primary_key=True) 
    movement_id = models.ForeignKey(WarehouseMovement, on_delete=models.CASCADE, db_column='movement_id', null=True)
    inventory_item_id = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, db_column='inventory_item_id', null=True)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'inventory"."warehouse_movement_items'
        managed = False  
        unique_together = (('movement_id', 'inventory_item_id'),)

    def __str__(self):
        return f"{self.warehouse_movement_items_id} - {self.inventory_item_id} ({self.quantity})"
    

    
class WarehouseMovementData(models.Model):
    movement_id = models.CharField(primary_key=True, max_length=50)
    movement_date = models.DateTimeField()
    source_location = models.CharField(max_length=255)
    destination_location = models.CharField(max_length=255)
    comments = models.TextField(null=True, blank=True)
    movement_status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'inventory"."vw_warehouse_movement_data'
