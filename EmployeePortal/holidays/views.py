from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import *
from django.http import JsonResponse
from .models import Holidays


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

class DeleteHoliday(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes =[IsAdminUser]
  
    # To delete holiday by id
    def delete(self,request,holiday_id):
        try:  
            holiday = Holidays.objects.get(pk= holiday_id)
            holiday.delete()
            return JsonResponse({"message":"Holiday deleted"},status=200) 
        except Exception as error:
            print(error)
            return JsonResponse({"error":str(error)},status=500)



class UpdateHoliday(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes =[IsAdminUser]

    #To update holiday by admin only
    def put(self, request, holiday_id):
        try:
            holiday = Holidays.objects.get(id=holiday_id)
        except Holidays.DoesNotExist:
            return JsonResponse({"message":"Holiday not found"}, status=404)

        serializer = HolidaySerializer(holiday, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Holiday updated successfully"},status=200)
        return JsonResponse({"error": 'serializer.errors'}, status=400)


class ViewHoliday(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes =[IsAuthenticated]

    #To view holidays by everyone
    def get(self, request):
        holidays = Holidays.objects.all()      
        serializer = HolidaySerializer(holidays, many=True)
        return JsonResponse({"Holidays": serializer.data}, status= 200)


