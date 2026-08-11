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

    self.category = Category.objects.create(name="Electronics")

    self.category_obj = Category.objects.create(name="Fashion")

    self.product = Product.objects.create(
      name="Iphone16",
      description="this is a very good phone.",
      price=1100,
      stock_quantity=20,
      category=self.category
    )

    self.data = {
      "name": "samsung",
      "description": "also a good product",
      "price": 900,
      "stock_quantity": 12,
      "category": self.category.id
    }

    self.category_list_url = reverse('category-list')

    self.category_detail_url = reverse('category-detail', kwargs={"category_id": self.category_obj.id})

    self.url = reverse('product-list')


  def test_get_product(self):
    self.client.force_authenticate(user=self.authenticated_user)
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)


  def test_unauthenticated_user_get_product(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 401)


  def test_admin_post_product(self):
    self.client.force_authenticate(self.admin_user)
    response = self.client.post(self.url, self.data)
    self.assertEqual(response.status_code, 201)

  def test_normal_user_post(self):
    response = self.client.post(self.url, self.data)
    self.assertEqual(response.status_code, 401)

  def test_authenticated_but_not_admin_post_product(self):
    self.client.force_authenticate(self.authenticated_user)
    response = self.client.post(self.url, self.data)
    self.assertEqual(response.status_code, 403)


  ########### test category api ##################

  def test_admin_user_get_category_list(self):
    self.client.force_authenticate(user=self.admin_user)
    response = self.client.get(self.category_list_url)
    self.assertEqual(response.status_code, 200)

  def test_authenticated_user_get_category_list(self):
    self.client.force_authenticate(user=self.authenticated_user)
    response = self.client.get(self.category_list_url)
    self.assertEqual(response.status_code, 200)

  def test_unauthenticated_user_get_category_list(self):
    response = self.client.get(self.category_list_url)
    self.assertEqual(response.status_code, 401)
  

  def test_admin_user_post_category(self):
    self.client.force_authenticate(user=self.admin_user)
    response = self.client.post(self.category_list_url, {"name": "makeup"})
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data['name'], "makeup")

  def test_authenticated_user_post_category(self):
    self.client.force_authenticate(user=self.authenticated_user)
    response = self.client.post(self.category_list_url, {"name": "makeup"})
    self.assertEqual(response.status_code, 403)

  def test_unauthenticated_user_post_category(self):
    response = self.client.post(self.category_list_url, {"name": "makeup"})
    self.assertEqual(response.status_code, 401)
  

  def test_admin_user_update_category(self):
    self.client.force_authenticate(user=self.admin_user)
    response = self.client.put(self.category_detail_url, {"name": "Beauty"})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data['name'], "Beauty")

  def test_authenticated_user_update_category(self):
    self.client.force_authenticate(user=self.authenticated_user)
    response = self.client.put(self.category_detail_url, {"name": "Beauty"})
    self.assertEqual(response.status_code, 403)

  def test_unauthenticated_user_update_category(self):
    response = self.client.put(self.category_detail_url, {"name": "Beauty"})
    self.assertEqual(response.status_code, 401)  


  def test_admin_user_delete_category(self):
    self.client.force_authenticate(user=self.admin_user)
    response = self.client.delete(self.category_detail_url)
    self.assertEqual(response.status_code, 204)

  def test_authenticated_user_delete_category(self):
    self.client.force_authenticate(user=self.authenticated_user)
    response = self.client.delete(self.category_detail_url)
    self.assertEqual(response.status_code, 403)

  def test_unauthenticated_user_delete_category(self):
    response = self.client.delete(self.category_detail_url)
    self.assertEqual(response.status_code, 401)