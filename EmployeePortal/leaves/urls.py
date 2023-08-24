from django.urls import path, include
from . import views


urlpatterns = [

    path('add', views.AddLeave.as_view())

]