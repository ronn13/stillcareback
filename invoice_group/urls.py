from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceGroupViewSet

router = DefaultRouter()
router.register(r'invoices', InvoiceGroupViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
] 