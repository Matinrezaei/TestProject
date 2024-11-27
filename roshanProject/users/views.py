from .serializers import CustomRegisterSerializer, CustomLoginSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from dj_rest_auth.views import LoginView



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CustomRegisterView(generics.CreateAPIView):
    serializer_class = CustomRegisterSerializer

class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

    def get_response(self):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=self.request.data,
                                      context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "Logout successful"})
    
