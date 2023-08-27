from django.urls import path, include
from . import views


urlpatterns = [

    path('add', views.AddLeave.as_view()),
    path('',views.ViewEmployeeLeaves.as_view()),
    path('admin', views.AdminLeave.as_view())

]