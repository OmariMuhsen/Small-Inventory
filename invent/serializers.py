# inventory/serializers.py
from rest_framework import serializers
from .models import Item, MaintenanceRecord, Transaction
from core.serializers import CategorySerializer, SupplierSerializer, LocationSerializer, PersonSerializer

class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    supplier = SupplierSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    assigned_to = PersonSerializer(read_only=True)

    class Meta:
        model = Item
        fields = '__all__'

class MaintenanceRecordSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    performed_by = PersonSerializer(read_only=True)

    class Meta:
        model = MaintenanceRecord
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    person = PersonSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    created_by = PersonSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
