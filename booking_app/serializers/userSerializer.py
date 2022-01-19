from rest_framework import serializers
from booking_app.models.userModel import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        token['name'] = user.name
        token['dni'] = user.dniUser
        token['role'] = user.role

        return token

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['dniUser','password','name','last_name','email','phone','role']
    
    def create(self, validated_data):
        userInstance = User.objects.create(**validated_data)
        return userInstance

    def to_representation(self, obj):
        user = User.objects.get(dniUser=obj.dniUser)
        return {
            'dniUser': user.dniUser,
            'name': user.name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'role': user.role
        }