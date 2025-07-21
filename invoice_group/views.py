from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import InvoiceGroup
from .serializers import InvoiceGroupSerializer

# Create your views here.

class InvoiceGroupViewSet(viewsets.ModelViewSet):
    queryset = InvoiceGroup.objects.all()
    serializer_class = InvoiceGroupSerializer
    
    def list(self, request, *args, **kwargs):
        """List all invoice groups with optional filtering"""
        queryset = self.get_queryset()
        
        # Filter by search term
        search = request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                description__icontains=search
            )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Create a new invoice group"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Update an invoice group"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """Delete an invoice group"""
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search invoice groups by name or description"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter "q" is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        invoice_groups = InvoiceGroup.objects.filter(
            name__icontains=query
        ) | InvoiceGroup.objects.filter(
            description__icontains=query
        )
        
        serializer = self.get_serializer(invoice_groups, many=True)
        return Response(serializer.data)
