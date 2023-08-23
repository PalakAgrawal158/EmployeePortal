from django.db import models

# Create your models here.

class Leaves(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid')]

    employee = models.ForeignKey("employee.Employee", on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices= LEAVE_TYPE_CHOICES)
    from_date = models.DateField()
    till_date = models.DateField()
    no_of_days = models.PositiveIntegerField()
    reason = models.TextField(max_length=35)
    status = models.CharField(default="Pending", max_length=20)