from django.db import models


class ItemMasterData(models.Model):
    item_id = models.CharField(
        db_column='item_id',
        primary_key=True,
        max_length=255
    )
    item_name = models.CharField(
        db_column='item_name',
        max_length=255
    )
    item_type = models.CharField(
        db_column='item_type',
        max_length=50,
        blank=True,
        null=True
    )
    unit_of_measure = models.CharField(
        db_column='unit_of_measure',
        max_length=50,
        blank=True,
        null=True
    )
    item_status = models.CharField(
        db_column='item_status',
        max_length=50,
        blank=True,
        null=True
    )
    manage_item_by = models.CharField(
        db_column='manage_item_by',
        max_length=50,
        blank=True,
        null=True
    )
    preferred_vendor = models.CharField(
        db_column='preferred_vendor',
        max_length=255,
        blank=True,
        null=True
    )
    purchasing_uom = models.CharField(
        db_column='purchasing_uom',
        max_length=50,
        blank=True,
        null=True
    )
    items_per_purchase_unit = models.IntegerField(
        db_column='items_per_purchase_unit',
        blank=True,
        null=True
    )
    purchase_quantity_per_package = models.IntegerField(
        db_column='purchase_quantity_per_package',
        blank=True,
        null=True
    )
    sales_uom = models.CharField(
        db_column='sales_uom',
        max_length=50,
        blank=True,
        null=True
    )
    items_per_sale_unit = models.IntegerField(
        db_column='items_per_sale_unit',
        blank=True,
        null=True
    )
    sales_quantity_per_package = models.IntegerField(
        db_column='sales_quantity_per_package',
        blank=True,
        null=True
    )
    item_description = models.TextField(
        db_column='item_description',
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = '"admin"."item_master_data"'

    def __str__(self):
        return f"{self.item_name} ({self.item_id})"


class InventoryItem(models.Model):
    inventory_item_id = models.CharField(
        db_column='inventory_item_id',  
        primary_key=True,
        max_length=255
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
        blank=True,
        null=True
    )
    expiry = models.DateTimeField(
        db_column='expiry',
        blank=True,
        null=True
    )
    shelf_life = models.CharField(
        db_column='shelf_life',
        max_length=50,
        blank=True,
        null=True
    )
    last_update = models.DateTimeField(
        db_column='last_update',
        auto_now=True
    )
    date_created = models.DateTimeField(
        db_column='date_created',
        auto_now_add=True
    )
    item = models.ForeignKey(
        ItemMasterData,
        db_column='item_id',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    item_no = models.CharField(
        db_column='item_no',
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )
    start_of_depreciation = models.DateTimeField(
        db_column='start_of_depreciation',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        db_column='is_active',
        default=True
    )
    is_demo_item = models.BooleanField(
        db_column='is_demo_item',
        default=False
    )

    class Meta:
        managed = False 
        db_table = '"inventory"."inventory_item"'

    def __str__(self):
        item_name = self.item.item_name if self.item else self.item_id
        return f"{item_name} - {self.item_no or self.inventory_item_id}"


class InventoryItemThreshold(models.Model):
    inventory_item_threshold_id = models.CharField(
        db_column='inventory_item_threshold_id',
        primary_key=True,
        max_length=255
    )
    item = models.ForeignKey(
        ItemMasterData,
        db_column='item_id',  
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    minimum_threshold = models.IntegerField(
        db_column='minimum_threshold'
    )
    maximum_threshold = models.IntegerField(
        db_column='maximum_threshold'
    )

    class Meta:
        managed = False
        db_table = '"inventory"."inventory_item_threshold"'  

    def __str__(self):
        item_name = self.item.item_name if self.item else self.item_id
        return f"Threshold for {item_name}: {self.minimum_threshold}-{self.maximum_threshold}"


class Purchase_requests(models.Model):
    request_id = models.CharField(
        primary_key=True,
        max_length=255
    )
    employee_id = models.CharField(  
        db_column='employee_id',
        max_length=255,
        blank=True,
        null=True
    )
    valid_date = models.DateField(
        db_column='valid_date',
        blank=True,
        null=True
    )
    document_date = models.DateField(
        db_column='document_date',
        blank=True,
        null=True
    )
    required_date = models.DateField(
        db_column='required_date',
        blank=True,
        null=True
    )
    status = models.CharField(
        db_column='status',
        max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = '"purchasing"."purchase_requests"'

    def __str__(self):
        return f"Request {self.request_id}"


class QuotationContent(models.Model):
    quotation_content_id = models.CharField(
        db_column='quotation_content_id',
        primary_key=True,
        max_length=255
    )
    request = models.ForeignKey(
        Purchase_requests,
        db_column='request_id',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    purchase_quantity = models.IntegerField(
        db_column='purchase_quantity',
        blank=True,
        null=True
    )
    unit_price = models.DecimalField(
        db_column='unit_price',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    discount = models.DecimalField(
        db_column='discount',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    tax_code = models.CharField(
        db_column='tax_code',
        max_length=50,
        blank=True,
        null=True
    )
    total = models.DecimalField(
        db_column='total',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    item = models.ForeignKey(
        ItemMasterData,
        db_column='item_id',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = '"purchasing"."quotation_contents"'

    def __str__(self):
        item_name = self.item.item_name if self.item else self.item_id
        return f"Content {self.quotation_content_id} for Item {item_name}"


class PurchaseQuotation(models.Model):
    quotation_id = models.CharField(
        db_column='quotation_id',
        primary_key=True,
        max_length=255
    )
    request = models.ForeignKey(
        Purchase_requests,
        db_column='request_id',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    vendor_code = models.CharField(
        db_column='vendor_code',
        max_length=255,
        blank=True,
        null=True
    )
    document_no = models.IntegerField(
        db_column='document_no',
        blank=True,
        null=True
    )
    valid_date = models.DateField(
        db_column='valid_date',
        blank=True,
        null=True
    )
    document_date = models.DateField(
        db_column='document_date',
        blank=True,
        null=True
    )
    required_date = models.DateField(
        db_column='required_date',
        blank=True,
        null=True
    )
    buyer = models.CharField(
        db_column='buyer',
        max_length=100,
        blank=True,
        null=True
    )
    remarks = models.TextField(
        db_column='remarks',
        blank=True,
        null=True
    )
    delivery_loc = models.CharField(
        db_column='delivery_loc',
        max_length=255,
        blank=True,
        null=True
    )
    downpayment_request = models.IntegerField(
        db_column='downpayment_request',
        default=0
    )
    total_before_discount = models.DecimalField(
        db_column='total_before_discount',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    discount_percent = models.DecimalField(
        db_column='discount_percent',
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )
    freight = models.DecimalField(
        db_column='freight',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    tax = models.DecimalField(
        db_column='tax',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    total_payment = models.DecimalField(
        db_column='total_payment',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    owner = models.CharField(
        db_column='owner',
        max_length=255,
        blank=True,
        null=True
    )
    status = models.CharField(
        db_column='status',
        max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = '"purchasing"."purchase_quotation"'

    def __str__(self):
        return f"Quotation {self.quotation_id}"


class ProductInventoryView(models.Model):
    item_id = models.CharField(primary_key=True, max_length=255)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    stock_committed = models.IntegerField(default=0)
    total_stock = models.IntegerField(default=0)
    available_stock = models.IntegerField(default=0)
    minimum_threshold = models.IntegerField(default=0)
    maximum_threshold = models.IntegerField(default=0)
    last_update = models.DateTimeField(null=True, blank=True)
    unit_of_measure = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"inventory"."vw_inventory_product_data"'
    
    def __str__(self):
        return f"Product Inventory: {self.item_name or self.item_id}"


class AssetInventoryView(models.Model):
    item_id = models.CharField(primary_key=True, max_length=255)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    stock_on_order = models.IntegerField(default=0)
    total_stock = models.IntegerField(default=0)
    minimum_threshold = models.IntegerField(default=0)
    maximum_threshold = models.IntegerField(default=0)
    last_update = models.DateTimeField(null=True, blank=True)
    unit_of_measure = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '"inventory"."vw_inventory_asset_data"'
    
    def __str__(self):
        return f"Asset Inventory: {self.item_name or self.item_id}"


class RawMaterialInventoryView(models.Model):
    item_id = models.CharField(primary_key=True, max_length=255)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    stock_on_order = models.IntegerField(default=0)
    total_stock = models.IntegerField(default=0)
    minimum_threshold = models.IntegerField(default=0)
    maximum_threshold = models.IntegerField(default=0)
    last_update = models.DateTimeField(null=True, blank=True)
    unit_of_measure = models.CharField(max_length=50, blank=True, null=True)
    earliest_expiry = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"inventory"."vw_inventory_material_data"'

    def __str__(self):
        return f"Material Inventory: {self.item_name or self.item_id}"


# --- WAREHOUSE SPECIFIC VIEW MODELS ---

class WarehouseProductStockView(models.Model):
    # Composite key from view: item_id || '-' || warehouse_id
    id = models.CharField(primary_key=True, max_length=511)
    item_id = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    warehouse_id = models.CharField(max_length=255)
    total_stock = models.IntegerField(default=0)
    stock_committed = models.IntegerField(default=0) # Placeholder
    available_stock = models.IntegerField(default=0) # Placeholder
    minimum_threshold = models.IntegerField(default=0)
    maximum_threshold = models.IntegerField(default=0)
    last_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"inventory"."vw_warehouse_product_stock"'

    def __str__(self):
        return f"Product Stock: {self.item_name or self.item_id} in Whs {self.warehouse_id}"

class WarehouseAssetStockView(models.Model):
    # Composite key from view: item_id || '-' || warehouse_id
    id = models.CharField(primary_key=True, max_length=511)
    item_id = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    warehouse_id = models.CharField(max_length=255)
    total_stock = models.IntegerField(default=0)
    stock_on_order = models.IntegerField(default=0) # Placeholder
    minimum_threshold = models.IntegerField(default=0)
    maximum_threshold = models.IntegerField(default=0)
    last_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"inventory"."vw_warehouse_asset_stock"'

    def __str__(self):
        return f"Asset Stock: {self.item_name or self.item_id} in Whs {self.warehouse_id}"

class WarehouseMaterialStockView(models.Model):
    # Composite key from view: item_id || '-' || warehouse_id
    id = models.CharField(primary_key=True, max_length=511)
    item_id = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    warehouse_id = models.CharField(max_length=255)
    total_stock = models.IntegerField(default=0)
    stock_on_order = models.IntegerField(default=0) # Placeholder
    minimum_threshold = models.IntegerField(default=0)
    maximum_threshold = models.IntegerField(default=0)
    last_update = models.DateTimeField(null=True, blank=True)
    unit_of_measure = models.CharField(max_length=50, blank=True, null=True)
    earliest_expiry = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"inventory"."vw_warehouse_material_stock"'

    def __str__(self):
        return f"Material Stock: {self.item_name or self.item_id} in Whs {self.warehouse_id}"

# --- COMBINED WAREHOUSE STOCK VIEW MODEL ---

class WarehouseAllItemStockView(models.Model):
    # Composite key from underlying views
    id = models.CharField(primary_key=True, max_length=511)
    item_id = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    warehouse_id = models.CharField(max_length=255)
    item_type = models.CharField(max_length=50) # Added field
    total_stock = models.IntegerField(default=0)
    stock_committed = models.IntegerField(default=0) # Placeholder/Combined
    available_stock = models.IntegerField(default=0) # Placeholder/Combined
    stock_on_order = models.IntegerField(default=0) # Placeholder/Combined
    minimum_threshold = models.IntegerField(default=0)
    maximum_threshold = models.IntegerField(default=0)
    last_update = models.DateTimeField(null=True, blank=True)
    unit_of_measure = models.CharField(max_length=50, blank=True, null=True)
    earliest_expiry = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = '"inventory"."vw_warehouse_all_item_stock"'

    def __str__(self):
        return f"{self.item_type} Stock: {self.item_name or self.item_id} in Whs {self.warehouse_id}"