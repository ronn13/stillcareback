from rest_framework import serializers
from .models import Client
from invoice_group.models import InvoiceGroup

class InvoiceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceGroup
        fields = ['id', 'name', 'description']

class ClientSerializer(serializers.ModelSerializer):
    invoice_group = InvoiceGroupSerializer(read_only=True)
    invoice_group_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    full_name = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    
    class Meta:
        model = Client
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'address',
            'care_checklist', 'invoice_group', 'invoice_group_id',
            'full_name', 'full_address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        invoice_group_id = validated_data.pop('invoice_group_id', None)
        if invoice_group_id:
            try:
                validated_data['invoice_group'] = InvoiceGroup.objects.get(id=invoice_group_id)
            except InvoiceGroup.DoesNotExist:
                pass
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        invoice_group_id = validated_data.pop('invoice_group_id', None)
        if invoice_group_id is not None:
            if invoice_group_id:
                try:
                    validated_data['invoice_group'] = InvoiceGroup.objects.get(id=invoice_group_id)
                except InvoiceGroup.DoesNotExist:
                    validated_data['invoice_group'] = None
            else:
                validated_data['invoice_group'] = None
        return super().update(instance, validated_data) 