from .serializers import OfficialRegisterSerializer , LoginSerializer , UserRegisterSerializer, OfficialUpdateSerializer, UserUpdateSerializer
from .models import official, User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from .utils import generate_otp, send_otp_email
from django.utils import timezone
from Complaints.utils import authenticate_user

class OfficialRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OfficialRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserRegistrationView(APIView):
    def UserRegister(self, request):

        serializer = UserRegisterSerializer(data=request.data)
        otp = generate_otp()
        email = serializer.validated_data["email"]
        user = User.object.filter(email=email).first()
        user_name = user.name

        if email == user.email:

            if user.is_verified:

                return Response({"message":"The email is already registered"})
            
            if user.is_otp_expired():

                user.generate_new_otp()
                send_otp_email(email, otp)
                return Response({"message": "New OTP has been sent to your email"}, status=status.HTTP_200_OK)
            
            else:

                return Response({"message": "An OTP has already been sent. Please check your email"}, status=status.HTTP_400_BAD_REQUEST)
            
        if serializer.is_valid():

            serializer.save(otp=otp, otp_created_at = timezone.now())
            send_otp_email(email, otp, user_name)
            return Response({"message": "Registration successful. Please check your email for OTP"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OTPVerificationView(APIView):
    def get(self, request):
        otp = request.GET.get('otp')
        email = request.GET.get('email')

        if not otp or not email:
            return Response({'error': 'Invalid parameters'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp != otp:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_otp_expired():
            return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.otp = None
        user.otp_created_at = None
        user.save()

        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)


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


class OfficialDetailsUpdation(APIView):
    def patch(self, request):
        token = request.COOKIES.get("jwt")
        user = authenticate_user(token)
        serializer = OfficialUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"The Details updated succesfully"},status=200)
        else:
            return Response({"Error":"Please provide proper details"},status=400)
        
        
    def post(self, request):
        response = Response({"message": "Logged out successfully"}, status=200)
        response.delete_cookie('jwt')
        return response
    
    
class UserDetailsUpdation(APIView):
    def patch(self, request):
        token = request.COOKIES.get("jwt")
        user = authenticate_user(token)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"The Details updated succesfully"},status=200)
        else:
            return Response({"Error":"Please provide proper details"},status=400)
        
        
    def post(self, request):
        response = Response({"message": "Logged out successfully"}, status=200)
        response.delete_cookie('jwt')
        return response
    
class WingHeadSelect(APIView):
    def post(self,request,official_id):
        token = request.COOKIES.get("jwt")
        user = authenticate_user(token)
        if not user.is_superuser:
            return Response({"Message":"You are not authorized to assign the wing"},status=403)
        else:
            try:
                official_person = official.objects.find(id=official_id)
                official_person.head_of_wing = True
                official_person.save()
                return Response({"Message":"The person is assigned as the head of the wing"},status=200)
            except official.DoesNotExist:
                return Response({"error":"The official not found"},status=404)