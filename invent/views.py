# backend/inventory/views.py
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Category, Supplier, Location, Person,
    Item, MaintenanceRecord, Transaction
)
from .serializers import (
    CategorySerializer, SupplierSerializer,
    LocationSerializer, PersonSerializer,
    ItemListSerializer, ItemDetailSerializer, ItemCreateUpdateSerializer,
    MaintenanceRecordSerializer, MaintenanceRecordCreateSerializer,
    TransactionSerializer, TransactionCreateSerializer
)
from .filters import ItemFilter, TransactionFilter
from .permissions import IsInventoryManagerOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsInventoryManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['parent']

    def get_queryset(self):
        return Category.objects.prefetch_related('children').all()

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsInventoryManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'email']

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, IsInventoryManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['parent_location']

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department', 'position']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsInventoryManagerOrReadOnly()]
        return super().get_permissions()

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    permission_classes = [IsAuthenticated, IsInventoryManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ItemFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ItemListSerializer
        elif self.action == 'retrieve':
            return ItemDetailSerializer
        return ItemCreateUpdateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related(
            'category', 'location', 'assigned_to', 'supplier'
        )
        return queryset

    @action(detail=True, methods=['get'])
    def maintenance_history(self, request, pk=None):
        item = self.get_object()
        records = item.maintenance_records.order_by('-date')
        page = self.paginate_queryset(records)
        if page is not None:
            serializer = MaintenanceRecordSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MaintenanceRecordSerializer(records, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def transaction_history(self, request, pk=None):
        item = self.get_object()
        transactions = item.transactions.order_by('-date')
        page = self.paginate_queryset(transactions)
        if page is not None:
            serializer = TransactionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        low_stock_items = self.get_queryset().filter(
            quantity__lte=models.F('minimum_quantity')
        )
        page = self.paginate_queryset(low_stock_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)

class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.all()
    permission_classes = [IsAuthenticated, IsInventoryManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['item', 'performed_by', 'date']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MaintenanceRecordCreateSerializer
        return MaintenanceRecordSerializer

    def get_queryset(self):
        return super().get_queryset().select_related('item', 'performed_by')

    def perform_create(self, serializer):
        serializer.save(performed_by=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TransactionCreateSerializer
        return TransactionSerializer

    def get_queryset(self):
        return super().get_queryset().select_related(
            'item', 'person', 'location', 'created_by'
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_transactions = self.get_queryset().order_by('-date')[:20]
        serializer = self.get_serializer(recent_transactions, many=True)
        return Response(serializer.data)

class DashboardViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        data = {
            'total_items': Item.objects.count(),
            'total_categories': Category.objects.count(),
            'low_stock_items': Item.objects.filter(
                quantity__lte=models.F('minimum_quantity')
            ).count(),
            'recent_transactions': TransactionSerializer(
                Transaction.objects.order_by('-date')[:5],
                many=True
            ).data,
            'pending_maintenance': MaintenanceRecordSerializer(
                MaintenanceRecord.objects.filter(date__gte=timezone.now()),
                many=True
            ).data,
        }
        return Response(data)