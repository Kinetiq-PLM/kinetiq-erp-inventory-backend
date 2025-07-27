from django.contrib import admin
from .models import (
    ItemMasterData,
    InventoryItem,
    InventoryItemThreshold,
    Purchase_requests,
    QuotationContent,
    PurchaseQuotation
)

admin.site.register(ItemMasterData)
admin.site.register(InventoryItem)
admin.site.register(InventoryItemThreshold)
admin.site.register(Purchase_requests)
admin.site.register(QuotationContent)
admin.site.register(PurchaseQuotation)
