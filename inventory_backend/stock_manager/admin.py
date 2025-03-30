from django.contrib import admin
from .models import (
    AdminItemMasterData,
    InventoryItemMasterData,
    Products,
    Assets,
    Raw_Materials,
    Purchase_requests
)

admin.site.register(AdminItemMasterData)
admin.site.register(InventoryItemMasterData)
admin.site.register(Products)
admin.site.register(Assets)
admin.site.register(Raw_Materials)
admin.site.register(Purchase_requests)
