from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Employee(User):

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    designation = models.CharField(max_length=20 )
    contact_no = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    date_of_birth = models.DateField()
    address = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now =True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["email","first_name","last_name","password","contact_no","address","designation"]

    

    def __str__(self):
        return self.email
    
class OTP(models.Model):
    employee = models.ForeignKey("employee.Employee",  on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)
    expiration_time = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expiration_time 


