from django.urls import path, include
from . import views


urlpatterns = [

    path('register', views.RegisterUser.as_view()),
    path('login', views.LoginUser.as_view()),
    path('list', views.ListEmployees.as_view()),
    path('details', views.EmployeeDetails.as_view()),
    path('otp', views.SendOTP.as_view()),
    path('verify', views.VerifyOTP.as_view()),
    path('password', views.ChangePassword.as_view()),
    path('update/<int:employee_id>', views.UpdateEmployee.as_view()),
    path('delete/<int:employee_id>', views.DeleteEmployee.as_view()),

    
]