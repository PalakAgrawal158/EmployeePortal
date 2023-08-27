from django.urls import path, include
from .views import SendEmail


urlpatterns = [

    path('send_email/', SendEmail),
    
]