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
    stock_level = models.IntegerField(
        db_column='stock_level',
        null=True,
        blank=True
    )
    warranty_period = models.IntegerField(
        db_column='warranty_period',
        null=True,
        blank=True
    )
    policy_id = models.CharField(
        db_column='policy_id',
        max_length=255,
        null=True,
        blank=True
    )
    batch_no = models.CharField(
        db_column='batch_no',
        max_length=255,
        null=True,
        blank=True
    )
    item_status = models.CharField(
        db_column='item_status',
        max_length=50,
        null=True,
        blank=True
    )
    content_id = models.CharField(
        db_column='content_id',
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

    class Meta:
        managed = False
        db_table = 'products'

    def __str__(self):
        return self.product_name

class Asset(models.Model):
    asset_id = models.CharField(
        db_column='asset_id',
        primary_key=True,
        max_length=255
    )
    asset_name = models.CharField(
        db_column='asset_name',
        max_length=255
    )
    purchase_date = models.DateField(
        db_column='purchase_date',
        null=True,
        blank=True
    )
    serial_no = models.CharField(
        db_column='serial_no',
        max_length=255,
        null=True,
        blank=True
    )
    purchased_price = models.DecimalField(
        db_column='purchase_price',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    content_id = models.CharField(
        db_column='content_id',
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'assets'

    def __str__(self):
        return self.asset_name


class RawMaterial(models.Model):
    material_id = models.CharField(
        db_column='material_id',
        primary_key=True,
        max_length=255
    )
    material_name = models.CharField(
        db_column='material_name',
        max_length=255
    )
    description = models.TextField(
        db_column='description',
        null=True,
        blank=True
    )
    unit_of_measure = models.CharField(
        db_column='unit_of_measure',
        max_length=50,
        null=True,
        blank=True
    )
    cost_per_unit = models.DecimalField(
        db_column='cost_per_unit',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    vendor_code = models.CharField(
        db_column='vendor_code',
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'raw_materials'

    def __str__(self):
        return self.material_name

class ItemMasterData(models.Model):
    item_id = models.CharField(
        db_column='item_id',
        primary_key=True,
        max_length=255
    )
    asset = models.ForeignKey(
        Asset,
        db_column='asset_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Product,
        db_column='product_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    material = models.ForeignKey(
        RawMaterial,
        db_column='material_id',
        on_delete=models.CASCADE,
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

class InventoryItemData(models.Model):
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
    material = models.ForeignKey(
        RawMaterial,
        db_column='material_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    asset = models.ForeignKey(
        Asset,
        db_column='asset_id',
        on_delete=models.CASCADE,
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
        auto_now_add=True
    )

    class Meta:
        managed = False 
        db_table = 'inventory_item'

    def __str__(self):
        return f"Inventory Item: {self.inventory_item_id}"


class InventoryItemThreshold(models.Model):
    inventory_item_threshold_id = models.CharField(
        db_column='inventory_item_threshold_id',
        primary_key=True,
        max_length=255
    )
    item = models.ForeignKey(
        ItemMasterData,
        db_column='item_id',  
        to_field='item_id',  
        on_delete=models.CASCADE,
        related_name='inventory_thresholds'
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
        return f"Threshold for {self.item.item_id}"

class Purchase_requests(models.Model):
    request_id = models.CharField(
        primary_key=True,
        max_length=255
    )
    employee_id = models.CharField(  
        max_length=255,
        null=True,
        blank=True
    )
    approval_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    valid_date = models.DateField(
        null=True,
        blank=True
    )
    document_date = models.DateField(
        null=True,
        blank=True
    )
    required_date = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'purchase_requests'

    def __str__(self):
        return f"Purchase Request: {self.request_id}"

class QuotationContent(models.Model):
    quotation_content_id = models.CharField(
        db_column='quotation_content_id',
        primary_key=True,
        max_length=255
    )
    request = models.ForeignKey(
        Purchase_requests,
        db_column='request_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    unit_price = models.DecimalField(
        db_column='unit_price',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    discount = models.DecimalField(
        db_column='discount',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    tax_code = models.CharField(
        db_column='tax_code',
        max_length=50,
        null=True,
        blank=True
    )
    total = models.DecimalField(
        db_column='total',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    material = models.ForeignKey(
        RawMaterial,
        db_column='material_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    asset = models.ForeignKey(
        Asset,
        db_column='asset_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    purchase_quantity = models.IntegerField(
        db_column='purchase_quantity',
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'quotation_contents'

    def __str__(self):
        if self.material:
            return f"Quotation Content for Material: {self.material.material_name}"
        elif self.asset:
            return f"Quotation Content for Asset: {self.asset.asset_name}"
        else:
            return f"Quotation Content: {self.quotation_content_id}"

class PurchaseQuotation(models.Model):
    quotation_id = models.CharField(
        db_column='quotation_id',
        primary_key=True,
        max_length=255
    )
    vendor_id = models.CharField(
        db_column='vendor_id',
        max_length=255,
        null=True,
        blank=True
    )
    request = models.ForeignKey(
        Purchase_requests,
        db_column='request_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'purchase_quotation'

    def __str__(self):
        return f"Purchase Quotation: {self.quotation_id}"

class ProductInventoryView(models.Model):
    """
    Maps to the vw_inventory_product_data database view.
    
    This view provides inventory information for products including:
    - stock_committed: Amount reserved in open orders
    - total_stock: Total physical inventory
    - available_stock: What's available for new orders (total_stock - stock_committed)
    - Threshold values for reordering
    """
    product_id = models.CharField(max_length=255, primary_key=True)
    stock_committed = models.IntegerField(default=0)
    total_stock = models.IntegerField(default=0)
    available_stock = models.IntegerField(default=0)
    minimum_threshold = models.IntegerField(default=0)
    maximum_threshold = models.IntegerField(default=0)
    last_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'vw_inventory_product_data'
    
    def __str__(self):
        return f"Inventory for {self.product_id}"

class AssetInventoryView(models.Model):
    """
    Maps to the vw_inventory_asset_data database view.
    
    This view provides inventory information for assets including:
    - stock_on_order: Quantity ordered from suppliers but not yet received
    - total_stock: Total physical inventory currently in warehouse
    - Threshold values for inventory management
    """
    asset_id = models.CharField(max_length=255, primary_key=True)
    stock_on_order = models.IntegerField(default=0)
    total_stock = models.IntegerField(default=0)
    minimum_threshold = models.IntegerField(default=0)
    maximum_threshold = models.IntegerField(default=0)
    last_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'vw_inventory_asset_data'
    
    def __str__(self):
        return f"Inventory for asset {self.asset_id}"

class RawMaterialInventoryView(models.Model):
    """
    Maps to the vw_inventory_material_data database view.
    
    This view provides inventory information for raw materials including:
    - stock_on_order: Quantity ordered from suppliers but not yet received
    - total_stock: Total physical inventory currently in warehouse
    - Threshold values for inventory management
    """
    material_id = models.CharField(max_length=255, primary_key=True)
    stock_on_order = models.IntegerField(default=0)
    total_stock = models.IntegerField(default=0)
    minimum_threshold = models.IntegerField(default=0)
    maximum_threshold = models.IntegerField(default=0)
    last_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'vw_inventory_material_data'
    
    def __str__(self):
        return f"Inventory for material {self.material_id}"