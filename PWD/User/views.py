from django.shortcuts import render
from .serializers import OfficialSerializer , LoginSerializer
from .models import official
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OfficialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = official.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("Invalid email")

        if not user.check_password(password):

            raise AuthenticationFailed("invalid password")

        payload = {
            "id": user.id,
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, "your_secret_key", algorithm="HS256")

        response = Response()
        response.set_cookie(
            key="jwt",
            value=token,
            httponly=False,
            samesite="None",
            secure=True,
            path="/",
        )
        response.data = {"jwt": token, "user": payload}
        return response


