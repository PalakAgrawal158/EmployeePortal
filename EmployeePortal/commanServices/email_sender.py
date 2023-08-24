from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import smtplib, ssl


@csrf_exempt

def SendEmail(generated_otp, email):
    try:
        port = 587  # For starttls
        smtp_server = settings.EMAIL_HOST
        sender_email = settings.EMAIL_HOST_USER
        receiver_email = "yogeshkunkawalekar@gmail.com"
        password = settings.EMAIL_HOST_PASSWORD
        message = f"""\
        Subject: Hi there

        This is your OTP - {generated_otp} """

        context = ssl.create_default_context()

        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        return True
    except Exception as error:
        print("Error", error)
        return False
        # return JsonResponse({"error": str(error)})