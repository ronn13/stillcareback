from rest_framework import serializers
from .models import InvoiceGroup
from client_management.models import Client

class InvoiceGroupSerializer(serializers.ModelSerializer):
    clients_count = serializers.SerializerMethodField()
    
    class Meta:
        model = InvoiceGroup
        fields = ['id', 'name', 'description', 'clients_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_clients_count(self, obj):
        return obj.clients.count() 