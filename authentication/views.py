from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def check_user_status(request):
    """
    Check if user exists and what authentication methods they have configured
    Used for the initial selection screen
    """
    username = request.data.get('username')
    
    if not username:
        return Response({
            'error': 'Username is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(username=username, is_staff_member=True, is_active=True)
        
        response_data = {
            'user_exists': True,
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.full_name,
            'has_login_code': bool(user.login_code),
            'has_biometric': bool(user.biometric_id),
            'available_methods': []
        }
        
        # Determine available authentication methods
        if user.has_usable_password():
            response_data['available_methods'].append('password')
        if user.has_login_code:
            response_data['available_methods'].append('pin')
        if user.has_biometric:
            response_data['available_methods'].append('biometric')
        
        return Response(response_data)
        
    except User.DoesNotExist:
        return Response({
            'user_exists': False,
            'message': 'User not found or not a staff member'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def setup_pin(request):
    """
    Setup PIN/login code for a user
    Requires username/password authentication first
    """
    username = request.data.get('username')
    password = request.data.get('password')
    login_code = request.data.get('login_code')
    
    if not all([username, password, login_code]):
        return Response({
            'error': 'Username, password, and login_code are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if len(login_code) != 6:
        return Response({
            'error': 'Login code must be exactly 6 digits'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Authenticate user first
    user = authenticate(username=username, password=password)
    if user is None or not user.is_staff_member:
        return Response({
            'error': 'Invalid username or password, or user is not a staff member'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check if login code is already taken
    if User.objects.filter(login_code=login_code).exclude(id=user.id).exists():
        return Response({
            'error': 'Login code is already in use by another user'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Set the login code
    user.login_code = login_code
    user.save()
    
    return Response({
        'message': 'PIN setup successful',
        'user_id': user.id,
        'username': user.username,
        'has_login_code': True
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def setup_biometric(request):
    """
    Setup biometric authentication for a user
    Requires username/password authentication first
    """
    username = request.data.get('username')
    password = request.data.get('password')
    biometric_id = request.data.get('biometric_id')
    
    if not all([username, password, biometric_id]):
        return Response({
            'error': 'Username, password, and biometric_id are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Authenticate user first
    user = authenticate(username=username, password=password)
    if user is None or not user.is_staff_member:
        return Response({
            'error': 'Invalid username or password, or user is not a staff member'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check if biometric ID is already taken
    if User.objects.filter(biometric_id=biometric_id).exclude(id=user.id).exists():
        return Response({
            'error': 'Biometric ID is already in use by another user'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Set the biometric ID
    user.biometric_id = biometric_id
    user.save()
    
    return Response({
        'message': 'Biometric setup successful',
        'user_id': user.id,
        'username': user.username,
        'has_biometric': True
    })


@api_view(['POST'])
def update_biometric(request):
    """
    Update biometric authentication for authenticated user
    """
    biometric_id = request.data.get('biometric_id')
    
    if not biometric_id:
        return Response({
            'error': 'Biometric ID is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    # Check if biometric ID is already taken by another user
    if User.objects.filter(biometric_id=biometric_id).exclude(id=user.id).exists():
        return Response({
            'error': 'Biometric ID is already in use by another user'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Update the biometric ID
    user.biometric_id = biometric_id
    user.save()
    
    return Response({
        'message': 'Biometric updated successfully',
        'user_id': user.id,
        'username': user.username,
        'has_biometric': True
    })


@api_view(['POST'])
def remove_biometric(request):
    """
    Remove biometric authentication for authenticated user
    """
    user = request.user
    
    # Remove the biometric ID
    user.biometric_id = None
    user.save()
    
    return Response({
        'message': 'Biometric removed successfully',
        'user_id': user.id,
        'username': user.username,
        'has_biometric': False
    })


@api_view(['POST'])
def remove_pin(request):
    """
    Remove PIN/login code for authenticated user
    """
    user = request.user
    
    # Remove the login code
    user.login_code = None
    user.save()
    
    return Response({
        'message': 'PIN removed successfully',
        'user_id': user.id,
        'username': user.username,
        'has_login_code': False
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login endpoint for mobile app authentication
    Supports username/password, login code, and biometric authentication
    """
    username = request.data.get('username')
    password = request.data.get('password')
    login_code = request.data.get('login_code')
    biometric_id = request.data.get('biometric_id')
    
    # Check if using biometric authentication
    if biometric_id:
        if not biometric_id:
            return Response({
                'error': 'Biometric ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(biometric_id=biometric_id, is_staff_member=True, is_active=True)
        except User.DoesNotExist:
            return Response({
                'error': 'Invalid biometric ID or user is not a staff member'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check if using login code authentication
    elif login_code:
        if not login_code or len(login_code) != 6:
            return Response({
                'error': 'Login code must be exactly 6 digits'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(login_code=login_code, is_staff_member=True, is_active=True)
        except User.DoesNotExist:
            return Response({
                'error': 'Invalid login code or user is not a staff member'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Traditional username/password authentication
    elif username and password:
        user = authenticate(username=username, password=password)
        if user is None or not user.is_staff_member:
            return Response({
                'error': 'Invalid username or password, or user is not a staff member'
            }, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({
            'error': 'Either username/password, login_code, or biometric_id is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Get or create token for the user
    token, created = Token.objects.get_or_create(user=user)
    
    # Prepare user data with role information
    user_data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': user.full_name,
        'email': user.email,
        'phone': user.phone,
        'role': user.role,
        'role_display': user.get_role_display(),
        'is_active': user.is_active,
        'is_staff_member': user.is_staff_member,
        'has_login_code': bool(user.login_code),
        'has_biometric': bool(user.biometric_id),
    }
    
    response_data = {
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'staff': user_data  # Include staff information in the response
    }
    
    return Response(response_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_code_view(request):
    """
    Dedicated endpoint for login code authentication
    """
    login_code = request.data.get('login_code')
    
    if not login_code:
        return Response({
            'error': 'Login code is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if len(login_code) != 6:
        return Response({
            'error': 'Login code must be exactly 6 digits'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(login_code=login_code, is_staff_member=True, is_active=True)
    except User.DoesNotExist:
        return Response({
            'error': 'Invalid login code or user is not a staff member'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Get or create token for the user
    token, created = Token.objects.get_or_create(user=user)
    
    # Prepare user data with role information
    user_data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': user.full_name,
        'email': user.email,
        'phone': user.phone,
        'role': user.role,
        'role_display': user.get_role_display(),
        'is_active': user.is_active,
        'is_staff_member': user.is_staff_member,
        'has_login_code': bool(user.login_code),
        'has_biometric': bool(user.biometric_id),
    }
    
    response_data = {
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'staff': user_data  # Include staff information in the response
    }
    
    return Response(response_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_biometric_view(request):
    """
    Dedicated endpoint for biometric authentication
    """
    biometric_id = request.data.get('biometric_id')
    
    if not biometric_id:
        return Response({
            'error': 'Biometric ID is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(biometric_id=biometric_id, is_staff_member=True, is_active=True)
    except User.DoesNotExist:
        return Response({
            'error': 'Invalid biometric ID or user is not a staff member'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Get or create token for the user
    token, created = Token.objects.get_or_create(user=user)
    
    # Prepare user data with role information
    user_data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': user.full_name,
        'email': user.email,
        'phone': user.phone,
        'role': user.role,
        'role_display': user.get_role_display(),
        'is_active': user.is_active,
        'is_staff_member': user.is_staff_member,
        'has_login_code': bool(user.login_code),
        'has_biometric': bool(user.biometric_id),
    }
    
    response_data = {
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'staff': user_data  # Include staff information in the response
    }
    
    return Response(response_data)


@api_view(['POST'])
def logout_view(request):
    """
    Logout endpoint - delete the user's token
    """
    try:
        # Delete the user's token
        request.user.auth_token.delete()
        return Response({
            'message': 'Successfully logged out'
        })
    except:
        return Response({
            'message': 'Successfully logged out'
        })


@api_view(['GET'])
def user_info(request):
    """
    Get current user information
    """
    user = request.user
    
    # Prepare user data with role information
    user_data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': user.full_name,
        'email': user.email,
        'phone': user.phone,
        'role': user.role,
        'role_display': user.get_role_display(),
        'is_active': user.is_active,
        'is_staff_member': user.is_staff_member,
        'has_login_code': bool(user.login_code),
        'has_biometric': bool(user.biometric_id),
    }
    
    response_data = {
        'user_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'staff': user_data  # Include staff information in the response
    }
    
    return Response(response_data)
