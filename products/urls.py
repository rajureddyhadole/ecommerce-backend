from django.urls import path
from .views import CategoryListCreateView, ProductListCreateView, ProductDetail, CategoryDetailView

urlpatterns = [
  path('products/', ProductListCreateView.as_view(), name="product-list"),
  path("products/<int:product_id>/", ProductDetail.as_view()),
  path('categories/', CategoryListCreateView.as_view()),
  path('categories/<int:category_id>/', CategoryDetailView.as_view()),
]