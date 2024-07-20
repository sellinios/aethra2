# users/serializers/login_serializer.py
from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError('Must include "username" and "password"')

        user = authenticate(username=username, password=password)
        if user:
            data['user'] = user
            return data

        raise serializers.ValidationError('Invalid username or password')