from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class APIEndpointTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.api_client = APIClient()

    def test_categories_url_status_code(self):
        url = reverse('categories')
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_sales_url_status_code(self):
        url = reverse('tasalesgs')
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_shops_url_status_code(self):
        url = reverse('shops')
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_forecast_url_status_code(self):
        url = reverse('forecast')
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)
