from django.contrib import admin
from .models import Assets, Raw_Materials, Products, InventoryItemMasterData, Purchase_requests

admin.site.register(Assets)
admin.site.register(Raw_Materials)
admin.site.register(Products)
admin.site.register(InventoryItemMasterData)
admin.site.register(Purchase_requests)
