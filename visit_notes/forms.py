from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content', 'document', 'uploaded_by']
        widgets = {
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        } 