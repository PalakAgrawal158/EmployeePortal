from .models import Holidays
from rest_framework import serializers

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model= Holidays
        fields= '__all__'



