# inventory/admin.py
from django.contrib import admin
from .models import (
    Category, Supplier, Location, Person,
    Item, MaintenanceRecord, Transaction
)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'location', 'assigned_to', 'category')
    list_filter = ('category', 'location', 'type')
    search_fields = ('name', 'serial_number', 'barcode')
    readonly_fields = ('created_at', 'updated_at')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('item', 'transaction_type', 'quantity', 'date', 'created_by')
    list_filter = ('transaction_type', 'date')
    date_hierarchy = 'date'
    readonly_fields = ('date', 'created_by')

admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Location)
admin.site.register(Person)
admin.site.register(Item, ItemAdmin)
admin.site.register(MaintenanceRecord)
admin.site.register(Transaction, TransactionAdmin)