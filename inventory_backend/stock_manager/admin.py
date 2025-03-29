from django.contrib import admin
from .models import Assets, Raw_Materials, Products, InventoryItemMasterData

admin.site.register(Assets)
admin.site.register(Raw_Materials)
admin.site.register(Products)
admin.site.register(InventoryItemMasterData)
