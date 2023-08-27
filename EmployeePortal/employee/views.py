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
from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth.models import User
import random
from datetime import timedelta
from django.utils import timezone
from commanServices.email_sender import SendEmail
from rest_framework.pagination import PageNumberPagination

# Create your views here.

def home(request):
    return render(request, 'home.html')

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
                return JsonResponse({"error": serializer.errors},status=400)     
        except Exception as error:
            return JsonResponse({"error": str(error)},status=500)

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
                    return JsonResponse({"message": "Invalid credentials."}, status=401)
            return JsonResponse({"message": serializer.errors},status=400)
       
        except Exception as error:
            print(error)
            return JsonResponse({"error": str(error)},status=500)


class ListEmployees(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    
    #List all employees to admin
    def get(self, request):
        try:
            employees = Employee.objects.filter(is_active=True)
          
            paginator= PageNumberPagination()
            paginator.page_size = 2

            paginated_employees = paginator.paginate_queryset(employees, request)

            serializer = EmployeeDetailsSerializer(paginated_employees, many=True)

            pagination_data={"total_employees": paginator.page.paginator.count,
                            "total_pages":paginator.page.paginator.num_pages,
                             "has_next": paginator.page.has_next(),
                             "has_previous": paginator.page.has_previous()
                             }

            return JsonResponse({"Employees":serializer.data,
                                 "pagination_data":pagination_data},status=200)
        except Exception as error:
            return JsonResponse({"error": "An unexpected error occurred: "+ str(error)},status=500)


class EmployeeDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    #View specific employee details
    def get(self, request):
        try:
            token = decode_token(request)
            if token:
                user_id = token.get('user_id') 
                if user_id is not None:              
                    employee = Employee.objects.filter(pk=user_id).values()
                    if not employee:
                        return JsonResponse({"message": "Employee not found"}, status=404)
                    serializer = EmployeeDetailsSerializer(employee, many=True)
                    return JsonResponse({"Employee":serializer.data},status=200)  
                else:
                    return JsonResponse({'error': 'Invalid or missing user_id in token'}, status=400)              
            else:
                return JsonResponse({'error': 'Authorization header missing'}, status=400)         
        except Exception as error:
                print("error ",error)
                return JsonResponse({"error": str(error)},status=500)


#To decode the jwt token 
def decode_token(request):
    try:
        header = request.headers.get('Authorization')

        if header and header.startswith('Bearer '):
            jwt_token = header.split(' ')[1]

            if jwt_token:
                payload =jwt_decode_handler(jwt_token)
                user_id = payload.get('user_id')
                if user_id is not None:
                    return payload 
                else:
                    print('Invalid user_id in JWT payload')
                    return False      
            else:
                return False
        else:
            print('JWT token not found in Authorization header')
            return False    
        
    except Exception as error:
                print('Error------>',error)
                return False
        

class SendOTP(APIView):
    # To send OTP to email
    def post(self, request):
        serializer = SendOTPSerializer(data= request.data)
        if serializer.is_valid():
            try:
                email = serializer.validated_data['email']

                generated_otp = str(random.randint(1000,9999))
                otp_expiry = timezone.now() +timedelta(minutes=1, seconds=30)
               
                employee = Employee.objects.get(email=email)
                
                otp_object = OTP(employee=employee, otp= generated_otp, expiration_time=otp_expiry)
                otp_object.save()
                result = SendEmail(generated_otp, email)
                if result: 
                    return JsonResponse({"message":"OTP sent successfully"}, status=200)
                else:
                    return JsonResponse({"message":"OTP not sent "}, status=400)
            except Employee.DoesNotExist:
                return JsonResponse({"message": "Employee not found." },status=401)
            except Exception as error:
                print("Error : ",error)
                return JsonResponse({"error": "An unexpected error occurred: "+ str(error)},status=500)
        return JsonResponse({"error ": serializer.errors}, status=400)


class VerifyOTP(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():
            try:
                email = serializer.validated_data['email']
                entered_otp = serializer.validated_data['otp']
            
                employee = Employee.objects.get(email=email)
                otp_object = OTP.objects.get(employee=employee, otp= entered_otp)

                # Check otp expiry time
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
            try:
                new_password = serializer.validated_data['new_password']

                request.user.set_password(new_password)
                request.user.save()
                
                return JsonResponse({"message":"Password changed successfully"},status=200)
            except Exception as error:
                return JsonResponse({"error": str(error)},status=500)
        else:
            return JsonResponse({"error": serializer.errors}, status=400)


class UpdateEmployee(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes =[IsAdminUser]

    #To update employee details by admin only
    def put(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return JsonResponse({"message":"Employee not found"}, status=404)

        serializer = EmployeeSerializer(employee, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Employee updated successfully"},status=200)
        return JsonResponse({"error": serializer.errors}, status=400)


class DeleteEmployee(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes =[IsAdminUser]
  
    # To delete employee by id change status is_active  to False
    def delete(self,request,employee_id):
        try:  
            employee = Employee.objects.get(pk= employee_id)
            employee.is_active = False
            employee.save()
            return JsonResponse({"message":"Employee deleted"},status=200) 
        except Employee.DoesNotExist:
            return JsonResponse({"message":"Employee not found"}, status=404)
        except Exception as error:
            print(error)
            return JsonResponse({"error":str(error)},status=500)




