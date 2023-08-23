from django.urls import path, include
from . import views


urlpatterns = [

    path('register', views.RegisterUser.as_view()),
    path('login', views.LoginUser.as_view()),
    # path('decode', views.ViewProfile.as_view()),
    path('list', views.ListEmployees.as_view()),
    path('details', views.EmployeeDetails.as_view()),
    path('otp', views.SendOTP.as_view()),
    path('verify', views.VerifyOTP.as_view()),
    path('password', views.ChangePassword.as_view()),

    # path('decode2', views.decode_token)
    
]