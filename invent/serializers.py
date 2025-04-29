
# backend/inventory/serializers.py
from rest_framework import serializers
from .models import Item, Person, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'email']

class ItemSerializer(serializers.ModelSerializer):
    assigned_to = PersonSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(), source='assigned_to', write_only=True, allow_null=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, allow_null=True
    )

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'quantity', 'category', 'category_id', 'assigned_to', 'assigned_to_id', 'created_at']
