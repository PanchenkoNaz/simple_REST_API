from rest_framework import viewsets, permissions
from .models import Category, MenuItem, Cart, Order
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'price', 'featured']
    search_fields = ['title']
    ordering_fields = ['price']
    ordering = ['price']  # Сортування за замовчуванням


# Кастомні дозволи для ролей
class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()

class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Delivery Crew').exists()

# Views
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]  # Лише менеджери

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsManager()]
        return [permissions.AllowAny()]  # Всі користувачі можуть переглядати меню

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]  # Лише аутентифіковані користувачі

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)  # Кожен користувач бачить свій кошик

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PATCH']:
            return [permissions.IsAuthenticated(), IsManager()]
        if self.request.user.groups.filter(name='Delivery Crew').exists():
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]
