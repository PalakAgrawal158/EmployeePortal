from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import HolidaySerializer
from django.http import JsonResponse
from .models import Holidays
from rest_framework import serializers


# Create your views here.

class AddHoliday(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes =[IsAdminUser]


    #To add holiday by admin only
    def post(self, request):
        serializer = HolidaySerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Holiday added successfully"},status=201)
        return JsonResponse({"error": serializer.errors}, status=400)

    # To delete holiday by id
    def delete(self,request):    
        holiday = Holidays.objects.get(pk= request.data['id'])
        holiday.delete()
        return JsonResponse({"message":"delete"})
   


class ViewHoliday(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes =[IsAuthenticated]

    #To view holidays by everyone
    def get(self, request):
        holidays = Holidays.objects.all().values_list()
        
        # serializer = HolidaySerializer(holidays, many=True)
        return JsonResponse({"Holidays": list(holidays)}, status= 200)




