from django.contrib import admin
from .models import Assets, Raw_materials, Products, ItemMasterData

admin.site.register(Assets)
admin.site.register(Raw_materials)
admin.site.register(Products)
admin.site.register(ItemMasterData)
