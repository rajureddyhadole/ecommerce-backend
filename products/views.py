from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
# Create your views here.


############## Product CRUD ######################

class ProductListCreateView(generics.ListCreateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer

  def get_permissions(self):
    if self.request.method == "POST":
      return [IsAdminUser()]
    return [IsAuthenticated()]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer

  lookup_url_kwarg = 'product_id'

  def get_permissions(self):
    if self.request.method == "PATCH" or self.request.method == "DELETE":
      return [IsAdminUser()]
    return [IsAuthenticated()]


################ Category CRUD #############

class CategoryListCreateView(generics.ListCreateAPIView):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer

  def get_permissions(self):
    if self.request.method == "POST":
      return [IsAdminUser()]
    return [IsAuthenticated()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  permission_classes = [IsAdminUser]

  lookup_url_kwarg = 'category_id'