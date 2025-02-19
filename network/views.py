from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsAdministrator
from .models import NetworkNode
from .serializers import NetworkNodeSerializer

class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.query_params.get('country', None)
        if country:
            queryset = queryset.filter(country=country)
        return queryset