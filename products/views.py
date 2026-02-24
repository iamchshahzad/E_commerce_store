from rest_framework import viewsets
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db import DatabaseError
from users.models import AdminActivity


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and (user.is_staff or getattr(user, "is_admin", False)))


def _log_admin_activity(request, *, action, object_repr, change_message, app_label, model):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return
    try:
        AdminActivity.objects.create(
            user=user,
            action=action,
            object_repr=object_repr[:255],
            change_message=change_message,
            app_label=app_label,
            model=model,
        )
    except DatabaseError:
        # Keep API actions working even if activity migration is pending.
        pass


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        product = serializer.save()
        _log_admin_activity(
            self.request,
            action="add_product",
            object_repr=str(product),
            change_message=f"Added product '{product.name}' with stock {product.stock}.",
            app_label="products",
            model="product",
        )

    def perform_update(self, serializer):
        previous = self.get_object()
        prev_stock = previous.stock
        prev_price = previous.price
        prev_category_id = previous.category_id
        prev_name = previous.name
        product = serializer.save()

        changes = []
        if product.stock != prev_stock:
            changes.append(f"stock: {prev_stock} -> {product.stock}")
        if product.price != prev_price:
            changes.append(f"price: {prev_price} -> {product.price}")
        if product.category_id != prev_category_id:
            changes.append(f"category: {prev_category_id} -> {product.category_id}")
        if product.name != prev_name:
            changes.append(f"name: {prev_name} -> {product.name}")

        action = "update_stock" if changes == [f"stock: {prev_stock} -> {product.stock}"] else "update_product"
        _log_admin_activity(
            self.request,
            action=action,
            object_repr=str(product),
            change_message=", ".join(changes) if changes else "Updated product.",
            app_label="products",
            model="product",
        )

    def perform_destroy(self, instance):
        object_repr = str(instance)
        super().perform_destroy(instance)
        _log_admin_activity(
            self.request,
            action="delete_product",
            object_repr=object_repr,
            change_message="Deleted product.",
            app_label="products",
            model="product",
        )

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        category = serializer.save()
        _log_admin_activity(
            self.request,
            action="add_category",
            object_repr=str(category),
            change_message=f"Added category '{category.name}'.",
            app_label="products",
            model="category",
        )

    def perform_update(self, serializer):
        previous = self.get_object()
        prev_name = previous.name
        category = serializer.save()
        _log_admin_activity(
            self.request,
            action="update_category",
            object_repr=str(category),
            change_message=f"name: {prev_name} -> {category.name}" if prev_name != category.name else "Updated category.",
            app_label="products",
            model="category",
        )

    def perform_destroy(self, instance):
        object_repr = str(instance)
        super().perform_destroy(instance)
        _log_admin_activity(
            self.request,
            action="delete_category",
            object_repr=object_repr,
            change_message="Deleted category.",
            app_label="products",
            model="category",
        )
