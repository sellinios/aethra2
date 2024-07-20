from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'preferred_language')  # Assuming these are the fields in your profile
        read_only_fields = ('username', 'email')  # Ensure username and email are read-only

    def update(self, instance, validated_data):
        instance.preferred_language = validated_data.get('preferred_language', instance.preferred_language)
        instance.save()
        return instance