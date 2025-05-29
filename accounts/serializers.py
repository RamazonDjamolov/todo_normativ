from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.models import User


class UserSerializer(ModelSerializer):
    re_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 're_password')

        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        re_password = attrs.pop('re_password')

        if password != re_password:
            raise serializers.ValidationError('Passwords do not match')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ListUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

