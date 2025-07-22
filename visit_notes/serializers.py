from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.ReadOnlyField(source='uploaded_by.username')
    class Meta:
        model = Note
        fields = ['id', 'content', 'document', 'uploaded_by', 'uploaded_by_username', 'created_at', 'updated_at']
        read_only_fields = ['id', 'uploaded_by', 'uploaded_by_username', 'created_at', 'updated_at'] 