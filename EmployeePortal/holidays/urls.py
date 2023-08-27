from django.urls import path, include
from . import views


urlpatterns = [

    path('add', views.AddHoliday.as_view()),
    path('',views.ViewHoliday.as_view()),
    path('<int:holiday_id>',views.UpdateHoliday.as_view()), 
    path('delete/<int:holiday_id>',views.DeleteHoliday.as_view())   
   

]