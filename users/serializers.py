from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'is_active', 'date_joined']
        read_only_field = ['is_active']


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance