from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet

router = DefaultRouter()
router.register(r'', NoteViewSet, basename='note')  # No prefix, so endpoints are directly under /api/notes/

urlpatterns = [
    path('create/<int:appointment_id>/', views.note_create, name='note_create'),
    path('edit/<int:note_id>/', views.note_edit, name='note_edit'),
    path('delete/<int:note_id>/', views.note_delete, name='note_delete'),
    path('detail/<int:note_id>/', views.note_detail, name='note_detail'),
]

urlpatterns += router.urls 