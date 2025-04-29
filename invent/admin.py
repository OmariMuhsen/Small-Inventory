# inventory/admin.py
from django.contrib import admin
from .models import Item, MaintenanceRecord, Transaction

admin.site.register(Item)
admin.site.register(MaintenanceRecord)
admin.site.register(Transaction)
