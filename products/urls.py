# products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 1. Create a router and register ViewSets
router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'categories', views.CategoryViewSet, basename='category')

# 2. Include the router URLs
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('api/', include(router.urls)),
]
