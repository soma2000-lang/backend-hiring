from rest_framework.reverse import reverse
from rest_framework.test import APISimpleTestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from website.constants.health import AppHealthStatus, ComponentHealthStatus


class HealthAPITests(APISimpleTestCase):
    def setUp(self):
        self.client = APIClient()

    def test_health_api_returns_200_when_db_healthy(self, mocked):
        url = reverse("health")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], AppHealthStatus.UP.name)
      

    def test_health_api_returns_503_when_db_not_healthy(self, mocked):
        url = reverse("health")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data["status"], AppHealthStatus.DOWN.name)
     