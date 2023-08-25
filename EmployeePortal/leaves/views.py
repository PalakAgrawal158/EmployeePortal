from django.shortcuts import render
from .models import Leaves
from employee.models import Employee
from rest_framework.views import APIView 
from django.http import JsonResponse
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from employee.views import decode_token
from rest_framework.pagination import PageNumberPagination


# Create your views here.


class AddLeave(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # To add leave by employee
    def post(self, request):
        try:
            token = decode_token(request)
            if token:
                user_id = token['user_id']
                try:    
                    employee = Employee.objects.get(pk=user_id)
                except Employee.DoesNotExist:
                    return JsonResponse({'error': 'Unauthorized user'}, status=401)
            else:
                return JsonResponse({'error': 'Authorization header missing'}, status=400)
        
            serializer = LeavesSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(employee=employee)
                return JsonResponse({'message' : 'Leave added successfully'},status=200) 
            else:
                return JsonResponse({"error": serializer.errors},status=status.HTTP_400_BAD_REQUEST)     
        except Exception as error:
            return JsonResponse({"error": str(error)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
    # To view applied leaves by employee
    def get(self, request):
        try:
            token = decode_token(request)
            if token:
                user_id = token['user_id']
                try:    
                    employee = Employee.objects.get(pk=user_id)
                except Employee.DoesNotExist:
                    return JsonResponse({'error': 'Unauthorized user'}, status=401)
            else:
                return JsonResponse({'error': 'Authorization header missing'}, status=400)
            
            leaves = Leaves.objects.filter (employee=employee)

            paginator= PageNumberPagination()
            paginator.page_size = 2

            paginated_leaves = paginator.paginate_queryset(leaves, request)

            serializer = AllLeavesSerializer(paginated_leaves , many=True)
            return JsonResponse({'Leaves' : serializer.data},status=200)
 
        except Exception as error:
            return JsonResponse({"error": str(error)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminLeave(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    #To view all pending leaves by admin
    def get(self, request):
        try:
            leaves = Leaves.objects.filter(status="Pending").values('id', 'from_date', 'till_date','leave_type', 'no_of_days', 'reason','employee_id','employee__first_name','employee__last_name' )
            return JsonResponse({'Leaves' : list(leaves)},status=200)
        except Exception as error:
            return JsonResponse({"error": str(error)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # To update the leave status by admin   
    def put(self, request):
        print(request.body)
        try:
            serializer = UpdateLeaveSerializer(data = request.data)

            if serializer.is_valid():
                leave_id = serializer.validated_data.get('leave_id')
                status = serializer.validated_data.get('status')
                
                try:
                    leave = Leaves.objects.get(pk=leave_id)
                except Leaves.DoesNotExist:
                    return JsonResponse({"error" : "Leave does not exist"}, status=404)
                
                leave.status = status
                leave.save()
                return JsonResponse({"message" : "Leave status updated"}, status=200)
            else:
                return JsonResponse({"error": serializer.errors},status=400)
        except Exception as error:
            return JsonResponse({"error": str(error)},status=500)

        





