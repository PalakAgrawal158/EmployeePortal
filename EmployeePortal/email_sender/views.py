from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import smtplib


@csrf_exempt

def SendEmail(request):
    try:
        li = ["yogesh.k@sankeysolutions.com"]
        s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        s.starttls()
        s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        message = "Message_you_need_to_send"
        s.sendmail(settings.EMAIL_HOST_USER,li, message)
        s.quit()
        return JsonResponse({"message":"Email sended Successfully"})
    except Exception as error:
        return JsonResponse({"error": str(error)})