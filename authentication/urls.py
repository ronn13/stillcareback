from django.urls import path
from . import views

urlpatterns = [
    # User status and setup endpoints
    path('check-user/', views.check_user_status, name='auth_check_user'),
    path('setup/pin/', views.setup_pin, name='auth_setup_pin'),
    path('setup/biometric/', views.setup_biometric, name='auth_setup_biometric'),
    
    # Login endpoints
    path('login/', views.login_view, name='auth_login'),
    path('login/code/', views.login_with_code_view, name='auth_login_code'),
    path('login/biometric/', views.login_with_biometric_view, name='auth_login_biometric'),
    
    # Management endpoints (require authentication)
    path('update/biometric/', views.update_biometric, name='auth_update_biometric'),
    path('remove/biometric/', views.remove_biometric, name='auth_remove_biometric'),
    path('remove/pin/', views.remove_pin, name='auth_remove_pin'),
    
    # Standard endpoints
    path('logout/', views.logout_view, name='auth_logout'),
    path('user/', views.user_info, name='auth_user_info'),
] 