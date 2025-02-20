from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models import CustomsUser

from .models import NetworkNode


class NetworkNodeModelTest(TestCase):
    def setUp(self):
        # Создание тестового объекта
        self.node = NetworkNode.objects.create(
            name="Завод TechPro",
            level=0,
            email="factory@techpro.com",
            country="Россия",
            city="Москва",
            street="Ленинская слобода",
            house_number="19",
            products=[
                {"name": "Смартфон X10", "model": "X10", "release_date": "2023-09-01"}
            ],
            debt=0.00,
        )

    def test_model_creation(self):
        # Проверка создания объекта
        self.assertEqual(NetworkNode.objects.count(), 1)
        self.assertEqual(self.node.name, "Завод TechPro")
        self.assertEqual(self.node.level, 0)

    def test_string_representation(self):
        # Проверка метода __str__
        self.assertEqual(str(self.node), "Завод TechPro")

    def test_filter_by_country(self):
        # Проверка фильтрации по стране
        nodes_in_russia = NetworkNode.objects.filter(country="Россия")
        self.assertEqual(nodes_in_russia.count(), 1)


class NetworkNodeViewSetTest(APITestCase):
    def setUp(self):
        # Создание тестовых данных
        self.client = APIClient()
        self.user = self.create_admin_user()
        self.node = NetworkNode.objects.create(
            name="Завод TechPro",
            level=0,
            email="factory@techpro.com",
            country="Россия",
            city="Москва",
            street="Ленинская слобода",
            house_number="19",
            products=[
                {"name": "Смартфон X10", "model": "X10", "release_date": "2023-09-01"}
            ],
            debt=0.00,
        )

    def create_admin_user(self):
        # Создание администратора
        return CustomsUser.objects.create_superuser(
            email="admin@example.com", password="adminpassword", is_staff=True
        )

    def authenticate_client(self):
        # Аутентификация клиента
        token_url = reverse("users:login")
        response = self.client.post(
            token_url, {"email": "admin@example.com", "password": "adminpassword"}
        )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_list_nodes(self):
        # Проверка получения списка звеньев сети
        self.authenticate_client()
        url = reverse("network:network-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_node(self):
        # Проверка создания нового звена сети
        self.authenticate_client()
        url = reverse("network:network-list")
        data = {
            "name": "ИП Иванов",
            "level": 2,
            "email": "ivanov@example.com",
            "country": "Россия",
            "city": "Москва",
            "street": "Большая Ордынка",
            "house_number": "12",
            "products": [
                {"name": "Наушники Buds", "model": "Buds", "release_date": "2023-08-10"}
            ],
            "supplier": None,
            "debt": 10000.00,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NetworkNode.objects.count(), 2)

    def test_unauthorized_access(self):
        # Проверка доступа без аутентификации
        url = reverse("network:network-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_by_country(self):
        # Проверка фильтрации по стране
        self.authenticate_client()
        url = reverse("network:network-list") + "?country=Россия"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
