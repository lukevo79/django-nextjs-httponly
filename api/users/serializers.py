from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import BpUser

class BpUserSerializer(ModelSerializer):
    class Meta:
        model = BpUser
        fields = ['id', 'username', 'email']

class RegisterUserSerializaer(ModelSerializer):
    class Meta:
        model = BpUser
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = BpUser.objects.create_user(**validated_data)
        return user 

class LoginUserSerializer(Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
