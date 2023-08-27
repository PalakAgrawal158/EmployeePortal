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
                user_id = token.get('user_id') 
                if user_id is not None:   
                    employee = Employee.objects.get(pk=user_id)
                else:
                    return JsonResponse({'error': 'Invalid or missing user_id in token'}, status=400)
            else:
                return JsonResponse({'error': 'Authorization header missing'}, status=400)
        
            serializer = LeavesSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(employee=employee)
                return JsonResponse({'message' : 'Leave added successfully'},status=200) 
            else:
                return JsonResponse({"error": serializer.errors},status=400)  
        except Employee.DoesNotExist:
                        return JsonResponse({'error': 'Unauthorized user'}, status=401)   
        except Exception as error:
            return JsonResponse({"error": str(error)},status=500)

class ViewEmployeeLeaves(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    # To retrieve applied leaves by an employee.
    def get(self, request):
        try:
            token = decode_token(request)
            if token:
                user_id = token.get('user_id') 
                if user_id is not None:     
                    try:
                        employee = Employee.objects.get(pk=user_id)
                    except Employee.DoesNotExist:
                        return JsonResponse({'error': 'Unauthorized user'}, status=401)
                else:
                    return JsonResponse({'error': 'Invalid or missing user_id in token'}, status=400)
            else:
                return JsonResponse({'error': 'Authorization header missing'}, status=400)
            
            leaves = Leaves.objects.filter(employee=employee).order_by('-from_date')

            if not leaves:
                return JsonResponse({"message": "No leaves found for this employee"}, status=404)

            #Pagination
            paginator= PageNumberPagination()
            paginator.page_size = 5

            paginated_leaves = paginator.paginate_queryset(leaves, request)

            serializer = AllLeavesSerializer(paginated_leaves , many=True)

            pagination_data={"total_leaves": paginator.page.paginator.count,
                            "total_pages":paginator.page.paginator.num_pages,
                             "has_next": paginator.page.has_next(),
                             "has_previous": paginator.page.has_previous()
                             }

            return JsonResponse({'Leaves' : serializer.data, 
                                 "pagination_data":pagination_data},status=200)    
        except Exception as error:
            return JsonResponse({"error": str(error)},status=500)


class AdminLeave(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    #To retrieve all pending leaves by admin
    def get(self, request):
        try:
            leaves = Leaves.objects.filter(status="Pending").values('id', 'from_date', 'till_date','leave_type', 'no_of_days', 'reason','employee_id','employee__first_name','employee__last_name' )
            return JsonResponse({'Leaves' : list(leaves)},status=200)
        except Exception as error:
            return JsonResponse({"error": str(error)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # To update the leave status by admin   
    def put(self, request):
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

        





