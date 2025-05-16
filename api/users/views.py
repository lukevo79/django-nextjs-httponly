from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from .serializers import BpUserSerializer, RegisterUserSerializaer, LoginUserSerializer

class UserInfoView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BpUserSerializer

    def get_object(self):
        return self.request.user
    
class UserRegistrationView(CreateAPIView):
    serializer_class = RegisterUserSerializaer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response = Response(
                {
                    'user'
                },
                status=status.HTTP_200_OK
            )
            response.set_cookie(key='access_token', value=access_token,
                                httponly=True,
                                secure=True,
                                samesite='None')
            response.set_cookie(key='refresh_token', value=str(refresh),
                                httponly=True,
                                secure=True,
                                samesite='None')
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
            except Exception as e:
                return Response({"error":"Error invalidating token:" + str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            response = Response({"message":"successfully logged out!"}, status=status.HTTP_200_OK)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response
        return Response({"error":"No refresh token found"}, status=status.HTTP_400_BAD_REQUEST)
    
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request):
        
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({"error":"Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = Response({"message":"Access Token refreshed successfully"}, status=status.HTTP_200_OK)
            response.set_cookie(key='access_token', value=access_token,
                                httponly=True,
                                secure=True,
                                samesite='None')
            return response
        except InvalidToken as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
    
    
    