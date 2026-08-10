from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from .models import Product, Category
# Create your tests here.

User = get_user_model()

class ProductAPITestCase(APITestCase):

  def setUp(self):
    self.admin_user = User.objects.create_superuser(username="admin_user", password="adminpass")
    self.authenticated_user = User.objects.create_user(username="auth_user", password="userpass")
    self.normal_user = User.objects.create_user(username="normal_user", password="otherpass")

    self.category = Category.objects.create(name="Electronics")

    self.product = Product.objects.create(
      name="Iphone16",
      description="this is a very good phone.",
      price=1100,
      stock_quantity=20,
      category=self.category
    )

    self.url = reverse('product-list')


  def test_get_product(self):

    self.client.force_authenticate(user=self.authenticated_user)

    response = self.client.get(self.url)

    self.assertEqual(response.status_code, 200)

