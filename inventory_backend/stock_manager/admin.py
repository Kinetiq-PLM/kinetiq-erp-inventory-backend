from django.contrib import admin
from .models import (
    ItemMasterData,
    InventoryItemData,
    InventoryItemThreshold,
    Product,
    Asset,
    RawMaterial,
    Purchase_requests
)

admin.site.register(ItemMasterData)
admin.site.register(InventoryItemData)
admin.site.register(InventoryItemThreshold)
admin.site.register(Product)
admin.site.register(Asset)
admin.site.register(RawMaterial)
admin.site.register(Purchase_requests)
