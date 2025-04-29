from rest_framework import serializers
from .models import Category, Supplier, Location, Person

# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

# Serializer for the Supplier model
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_person', 'email', 'phone', 'address', 'website', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

# Serializer for the Location model
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'description', 'address', 'parent_location', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

# Serializer for the Person model
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'email', 'phone', 'department', 'position', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
