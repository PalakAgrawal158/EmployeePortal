from django.urls import path, include
from . import views


urlpatterns = [

    path('add', views.AddHoliday.as_view()),
    path('',views.ViewHoliday.as_view())   

]