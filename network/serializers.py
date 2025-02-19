from rest_framework import serializers
from .models import NetworkNode

class NetworkNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = '__all__'
        read_only_fields = ('debt', 'created_at')  # Запрет обновления поля "debt" через API