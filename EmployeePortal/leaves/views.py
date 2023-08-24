from django.shortcuts import render
from .models import Leaves
from rest_framework.views import APIView 
from django.http import JsonResponse
from rest_framework import status
from .serializers import LeavesSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_jwt.utils import jwt_decode_handler
# Create your views here.

class AddLeave(APIView):
    def post(self, request):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        def post(self, request):
            try:
                header = request.headers.get('Authorization')

                if header and header.startswith('Bearer '):
                    jwt_token = header.split(' ')[1]

                    if jwt_token:
                            payload =jwt_decode_handler(jwt_token)
                            user_id = payload['user_id']
                else:
                    return JsonResponse({'error': 'Authorization header missing'}, status=401)
        
                serializer = LeavesSerializer(data = request.data)

                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message' : 'Leave added successfully'},status=200) 
                else:
                    return JsonResponse({"error": serializer.errors},status=status.HTTP_400_BAD_REQUEST)     
            except Exception as error:
                return JsonResponse({"error": str(error)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)





