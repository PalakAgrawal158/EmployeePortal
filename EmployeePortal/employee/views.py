from django.shortcuts import render
from rest_framework.views import APIView 
from django.http import JsonResponse
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Employee, OTP
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
import jwt
from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth.models import User
import random
from datetime import timedelta
from django.utils import timezone
from commanServices.email_sender import SendEmail

# Create your views here.


class RegisterUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    #Employee registered by admin only
    def post(self, request):
        try:
            serializer = EmployeeSerializer(data = request.data)

            if serializer.is_valid():
                user = serializer.save()
                return JsonResponse({'message' : 'Employee registered successfully'},status=200) 
            else:
                return JsonResponse({"error": serializer.errors},status=status.HTTP_400_BAD_REQUEST)     
        except Exception as error:
            return JsonResponse({"error": str(error)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Login can be accessed by anyone
class LoginUser(APIView):
    def post(self, request):
        try:            
            serializer = LoginSerializer(data = request.data)
                        
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password') 
                                      
                user = authenticate(request=request, username=email, password=password)
                
                if user is not None:
                    refresh = RefreshToken.for_user(user)
                    return JsonResponse({"refresh": str(refresh),
                                        "access": str(refresh.access_token),
                                        "message": "Login successful", 
                                        "is_admin": user.is_superuser
                                        }, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
            return JsonResponse({"message": serializer.errors},status=status.HTTP_400_BAD_REQUEST)
       
        except Exception as error:
            print(error)
            return JsonResponse({"error": str(error)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ListEmployees(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    
    #List all employees to admin
    def get(self, request):
        try:
            employees = Employee.objects.all()
            serializer = EmployeeSerializer(employees, many=True)
            return JsonResponse({"Employees":serializer.data},status= status.HTTP_200_OK)
        except Exception as error:
            return JsonResponse({"error": str(error)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class EmployeeDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    #View specific employee details
    def get(self, request):
        token = decode_token(request)
        if token:
            user_id = token['user_id']
            try:
                employee = Employee.objects.filter(pk=user_id).values()
                if not employee:
                    return JsonResponse({"message": "Employee not found"}, status=401)
                serializer = EmployeeSerializer(employee, many=True)
                return JsonResponse({"Employee":serializer.data},status= status.HTTP_200_OK)
            except Exception as error:
                return JsonResponse({"error": str(error)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)


#To decode the jwt token 
def decode_token(request):
    header = request.headers.get('Authorization')

    if header and header.startswith('Bearer '):
        jwt_token = header.split(' ')[1]

        if jwt_token:
            try:
                payload =jwt_decode_handler(jwt_token)
                user_id = payload['user_id']
                # user = Employee.objects.filter(pk=user_id).values()
                return payload
            
            except Exception as error:
                print('Error------>',error)
                return False        
        else:
            return False
        

class SendOTP(APIView):
    #to send OTP to email
    def post(self, request):
        serializer = SendOTPSerializer(data= request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            generated_otp = str(random.randint(1000,9999))
            otp_expiry = timezone.now() +timedelta(minutes=5)

            try:
                employee = Employee.objects.get(email=email)
            except Employee.DoesNotExist:
                return JsonResponse({"message": "Employee not found." },status=404)
            
            otp_object = OTP(employee=employee, otp= generated_otp, expiration_time=otp_expiry)
            otp_object.save()
            result = SendEmail(generated_otp, email)
            if result: 

                return JsonResponse({"message":"OTP sent successfully"}, status=200)
            else:
                return JsonResponse({"message":"OTP not sent "}, status=400)
        return JsonResponse({"error ": serializer.errors}, status=400)

class VerifyOTP(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            entered_otp = serializer.validated_data['otp']

            try:
                employee = Employee.objects.get(email=email)
                otp_object = OTP.objects.get(employee=employee, otp= entered_otp)

                if not otp_object.is_expired():
                    otp_object.delete()

                    refresh = RefreshToken.for_user(employee)

                    return JsonResponse({"message": "OTP varified successfully",
                                         "refresh": str(refresh),
                                         "access": str(refresh.access_token)
                                         }, status=200)
                else:
                    return JsonResponse({"message": "OTP has expired"}, status=400) 
            except (Employee.DoesNotExist, OTP.DoesNotExist):
                return JsonResponse({"message": "Invalid OTP"}, status=400)
        return JsonResponse({"error": serializer.errors}, status=400)
    
    

# To change password after OTP verification
class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']

            try:
                request.user.set_password(new_password)
                request.user.save()
                
                return JsonResponse({"message":"Password changed successfully"},status= status.HTTP_200_OK)
            except Exception as error:
                return JsonResponse({"error": str(error)},status=500)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)



