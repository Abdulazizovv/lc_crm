from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


User = get_user_model()

class TokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=400)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({'access_token': access_token, 'refresh_token': refresh_token})

class UserRegistrationView(APIView):
        permission_classes = [AllowAny]
            
        def post(self, request):
            email = request.data.get('email')
            password = request.data.get('password')
            phone_number = request.data.get('phone_number')
                
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already registered'}, status=400)
                
            # Create a new user
            user = User.objects.create_user(email=email, password=password, phone_number=phone_number)
              
            # Generate tokens for the new user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
               
            return Response({'access_token': access_token, 'refresh_token': refresh_token})