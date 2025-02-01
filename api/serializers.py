from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Notes, UserProfile


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notes
        fields=('id', 'user', 'title', 'body', 'created_at', 'updated_at')
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
        
    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email address is already taken.")
        return value
        
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'phone', 'created_at')
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return UserProfile.objects.create(user=user, **validated_data)
        