from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(InventoryItem)
admin.site.register(Employee)
admin.site.register(CyclicCount)
admin.site.register(ProductData)
