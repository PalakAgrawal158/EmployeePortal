from rest_framework import serializers
from .models import Leaves

class LeavesSerializer(serializers.ModelSerializer):
    class Meta :
        model = Leaves
        fields = '__all__'
        