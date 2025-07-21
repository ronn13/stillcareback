from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for API viewsets
router = DefaultRouter()
router.register(r'api/staff/appointments', views.StaffAppointmentViewSet, basename='staff-appointment')
router.register(r'api/staff/seizures', views.SeizureViewSet, basename='staff-seizure')
router.register(r'api/staff/incidents', views.IncidentViewSet, basename='staff-incident')
router.register(r'api/staff/medications', views.MedicationViewSet, basename='staff-medication')
router.register(r'api/staff/body-maps', views.BodyMapViewSet, basename='staff-body-map')

# Traditional Django URL patterns
urlpatterns = [
    # Traditional Django views
    path('', views.AppointmentListView.as_view(), name='appointment-list'),
    path('create/', views.AppointmentCreateView.as_view(), name='appointment-create'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('<int:pk>/edit/', views.AppointmentUpdateView.as_view(), name='appointment-update'),
    path('<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='appointment-delete'),
]

# Add API URLs
urlpatterns += router.urls

# Additional API endpoints
urlpatterns += [
    # Staff dashboard
    path('api/staff/dashboard/', views.StaffDashboardAPIView.as_view(), name='staff-dashboard'),
    
    # Mobile sync endpoint
    path('api/staff/sync/', views.MobileSyncAPIView.as_view(), name='mobile-sync'),
    
    # Include DRF browsable API
    path('api-auth/', include('rest_framework.urls')),
] 