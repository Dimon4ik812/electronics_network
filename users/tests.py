from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CustomsUser


class IsAdministratorPermissionTest(APITestCase):
    def setUp(self):
        # Создание пользователя и администратора
        self.user = CustomsUser.objects.create_user(
            email="user@example.com", password="userpassword"
        )
        self.admin = CustomsUser.objects.create_superuser(
            email="admin@example.com", password="adminpassword", is_staff=True
        )

    def test_authenticated_admin_access(self):
        # Проверка доступа для администратора
        self.client.force_authenticate(user=self.admin)
        url = reverse("network:network-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_access(self):
        # Проверка отсутствия доступа для обычного пользователя
        self.client.force_authenticate(user=self.user)
        url = reverse("network:network-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_access(self):
        # Проверка отсутствия доступа для неаутентифицированных пользователей
        url = reverse("network:network-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CustomsUserCreationTest(APITestCase):
    def test_create_user(self):
        # Проверка создания нового пользователя
        url = reverse("users:register")
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            CustomsUser.objects.filter(email="newuser@example.com").exists()
        )

    def test_invalid_user_creation(self):
        # Проверка создания пользователя с некорректными данными
        url = reverse("users:register")
        data = {
            "email": "invalid_email",  # Некорректный email
            "password": "short",  # Короткий пароль
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class JWTAuthenticationTest(APITestCase):
    def setUp(self):
        # Создание пользователя
        self.user = CustomsUser.objects.create_user(
            email="user@example.com", password="userpassword"
        )

    def test_obtain_token(self):
        # Проверка получения токена
        url = reverse("users:login")
        data = {"email": "user@example.com", "password": "userpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_refresh_token(self):
        # Проверка обновления токена
        url_obtain = reverse("users:login")
        data = {"email": "user@example.com", "password": "userpassword"}
        response_obtain = self.client.post(url_obtain, data, format="json")
        refresh_token = response_obtain.data["refresh"]

        url_refresh = reverse("users:token_refresh")
        response_refresh = self.client.post(
            url_refresh, {"refresh": refresh_token}, format="json"
        )
        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)
        self.assertIn("access", response_refresh.data)
