# core/admin.py
from django.contrib import admin
from .models import Category, Supplier, Location, Person

admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Location)
admin.site.register(Person)
