from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkNodeViewSet

app_name = "network"

router = DefaultRouter()
router.register(r'network', NetworkNodeViewSet, basename="network")

urlpatterns = [
    path('', include(router.urls)),
]