from rest_framework import serializers
from authentication.models import CustomUser,Hospital,Clinic
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_framework.fields import CurrentUserDefault


class RegistrationSerializer(serializers.ModelSerializer): 

    class Meta:
        model=CustomUser 
        fields=['phone','email','password','role','username']
        extra_kwargs={'password':{'write_only':True}}  

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user      

class HospitalRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model=Hospital
        #fields=['name','phone','address','registration_no','beds']
        fields=['name','phone','city', 'town', 'registration_no','beds']


    def create(self,validated_data):
        hospital=Hospital(**validated_data)
        hospital.save()
        return hospital



JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER        


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email':user.email,
            'token': jwt_token
        }