from django.db import models


# Bridge Models (placeholders for foreign key relationships)
class ItemMasterData(models.Model):
    item_id = models.CharField(max_length=255, primary_key=True)
    # Add minimal fields if needed, e.g., item_type, but only what's necessary for now

    class Meta:
        db_table = 'admin"."item_master_data'  # Matches your SQL schema
        managed = False  # Table already exists in DB

    def __str__(self):
        return self.item_id

class Warehouse(models.Model):
    warehouse_id = models.CharField(max_length=255, primary_key=True)
    # Add minimal fields if needed, e.g., warehouse_location

    class Meta:
        db_table = 'admin"."warehouse'  # Matches your SQL schema
        managed = False

    def __str__(self):
        return self.warehouse_id

class PurchaseOrder(models.Model):
    purchase_id = models.CharField(max_length=255, primary_key=True)
    # Add minimal fields if needed

    class Meta:
        db_table = 'purchasing"."purchase_order'  # Matches your SQL schema
        managed = False

    def __str__(self):
        return self.purchase_id

class Order(models.Model):
    order_id = models.CharField(max_length=255, primary_key=True)
    # Add minimal fields if needed

    class Meta:
        db_table = 'sales"."order'  # Matches your SQL schema
        managed = False

    def __str__(self):
        return self.order_id

# Main Model for warehouse_movement
class WarehouseMovement(models.Model):
    movement_id = models.CharField(max_length=255, primary_key=True)
    item = models.ForeignKey(
        ItemMasterData,
        on_delete=models.CASCADE,
        db_column='item_id'
    )
    movement_type = models.CharField(max_length=255)  # Text field in SQL, adjust length as needed
    quantity = models.IntegerField()
    movement_date = models.DateTimeField()
    destination = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        db_column='destination',
        related_name='destination_movements'
    )
    source = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        db_column='source',
        related_name='source_movements'
    )
    reference_id_purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        db_column='reference_id_purchase_order',
        null=True,
        blank=True
    )
    reference_id_order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        db_column='reference_id_order',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'inventory"."warehouse_movement'  # Matches your schema
        managed = False  # Table already exists in DB

    def __str__(self):
        return f"{self.movement_id} - {self.movement_type}"