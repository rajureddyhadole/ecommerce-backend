from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Cart, CartItem
from django.contrib.auth import get_user_model
from products.models import Product, Category
# Create your tests here.

User = get_user_model()

class CategoryAPITestCase(APITestCase):

  def setUp(self):
    self.user = User.objects.create(username="user", password="userpass")
    self.other = User.objects.create(username="other", password="otherpass")

    self.category = Category.objects.create(name="Shoes")

    self.product = Product.objects.create(
      name="Iphone16",
      description="this is a very good phone.",
      price=1100,
      stock_quantity=20,
      category=self.category
    )

    self.cart = Cart.objects.create(user=self.other)
    self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=10)

    self.url = reverse('cart-list')

  def test_user_cannot_get_other_users_cart_items(self):
    self.client.force_authenticate(user=self.user)
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data["data"], [])