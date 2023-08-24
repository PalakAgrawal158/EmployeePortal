from rest_framework import serializers
from .models import Leaves

class LeavesSerializer(serializers.ModelSerializer):
    class Meta :
        model = Leaves
        fields =['leave_type', 'from_date', 'till_date', 'no_of_days','reason']
        # fields = '__all__'

        def create(self, validated_data):
            user = Leaves(leave_type = validated_data["leave_type"],
                            from_date = validated_data['from_date'],
                            till_date = validated_data['till_date'],
                            no_of_days = validated_data['no_of_days'],
                            reaason = validated_data['reason']
                            )
            
class AllLeavesSerializer(serializers.ModelSerializer):
    class Meta :
        model = Leaves
        fields = '__all__'
    
class UpdateLeaveSerializer(serializers.Serializer):
    leave_id = serializers.CharField()
    status = serializers.CharField()

        