from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta :
        model = Employee
        # fields = '__all__'
        fields = ['email','password','first_name', 'last_name', 'contact_no', 'address','designation','blood_group','date_of_birth','created_at','modified_at']
        extra_kwargs = {
               'password' : {'write_only': True}
                        }
    
    def create(self, validated_data):
        user = Employee(username = validated_data['email'],
                           email = validated_data['email'],
                           first_name = validated_data['first_name'],
                           last_name = validated_data['last_name'],
                           contact_no = validated_data['contact_no'],
                           address = validated_data['address'],
                           designation = validated_data['designation'],
                           blood_group = validated_data['blood_group'],
                           date_of_birth = validated_data['date_of_birth']
                        
                           )
        user.set_password(validated_data['password'])
        user.save()
        return user
        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)

class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)



        