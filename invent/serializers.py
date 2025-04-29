# backend/inventory/serializers.py
from rest_framework import serializers
from .models import (
    Category, Supplier, Location, Person, 
    Item, MaintenanceRecord, Transaction
)

class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'parent', 
            'children', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_children(self, obj):
        children = Category.objects.filter(parent=obj)
        return CategorySerializer(children, many=True).data

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'contact_person', 'email', 
            'phone', 'address', 'website', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class LocationSerializer(serializers.ModelSerializer):
    parent_location = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = [
            'id', 'name', 'description', 'address',
            'parent_location', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'id', 'name', 'email', 'phone', 
            'department', 'position', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ItemListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    location = serializers.StringRelatedField()
    assigned_to = serializers.StringRelatedField()
    supplier = serializers.StringRelatedField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'type', 'quantity', 
            'minimum_quantity', 'unit', 'category',
            'location', 'assigned_to', 'supplier',
            'serial_number', 'barcode', 'status'
        ]

    def get_status(self, obj):
        if obj.quantity <= obj.minimum_quantity:
            return 'Needs Restock'
        return 'In Stock'

class ItemDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    assigned_to = PersonSerializer(read_only=True)
    supplier = SupplierSerializer(read_only=True)
    maintenance_records = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description', 'type',
            'quantity', 'minimum_quantity', 'unit',
            'category', 'location', 'assigned_to',
            'supplier', 'purchase_date', 'purchase_price',
            'serial_number', 'barcode', 'notes',
            'is_active', 'created_at', 'updated_at',
            'maintenance_records', 'transactions'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_maintenance_records(self, obj):
        records = obj.maintenance_records.order_by('-date')[:5]
        return MaintenanceRecordSerializer(records, many=True).data

    def get_transactions(self, obj):
        transactions = obj.transactions.order_by('-date')[:10]
        return TransactionSerializer(transactions, many=True).data

class ItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'name', 'description', 'type', 'quantity',
            'minimum_quantity', 'unit', 'category',
            'location', 'assigned_to', 'supplier',
            'purchase_date', 'purchase_price',
            'serial_number', 'barcode', 'notes', 'is_active'
        ]

class MaintenanceRecordSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()
    performed_by = PersonSerializer(read_only=True)

    class Meta:
        model = MaintenanceRecord
        fields = [
            'id', 'item', 'date', 'performed_by',
            'description', 'cost', 'notes', 'created_at'
        ]
        read_only_fields = ['created_at']

class MaintenanceRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = [
            'item', 'date', 'performed_by',
            'description', 'cost', 'notes'
        ]

class TransactionSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()
    person = PersonSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    created_by = PersonSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'item', 'transaction_type', 'quantity',
            'person', 'location', 'date', 'notes',
            'created_by'
        ]

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'item', 'transaction_type', 'quantity',
            'person', 'location', 'notes'
        ]

    def validate(self, data):
        item = data['item']
        transaction_type = data['transaction_type']
        quantity = data['quantity']

        if transaction_type in ['checkout', 'discard']:
            if quantity > item.quantity:
                raise serializers.ValidationError(
                    f"Cannot {transaction_type} more than available quantity ({item.quantity})"
                )
        return data

    def create(self, validated_data):
        item = validated_data['item']
        transaction_type = validated_data['transaction_type']
        quantity = validated_data['quantity']

        # Update item quantity based on transaction type
        if transaction_type == 'checkout':
            item.quantity -= quantity
        elif transaction_type == 'checkin':
            item.quantity += quantity
        elif transaction_type == 'restock':
            item.quantity += quantity
        elif transaction_type == 'discard':
            item.quantity -= quantity

        item.save()
        transaction = Transaction.objects.create(**validated_data)
        return transaction