from rest_framework import viewsets

from users.permissions import IsAdministrator

from .models import NetworkNode
from .serializers import NetworkNodeSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsAdministrator]

    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.query_params.get("country", None)
        if country:
            queryset = queryset.filter(country=country)
        return queryset
