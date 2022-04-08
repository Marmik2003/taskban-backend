from pathlib import Path

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from taskban_backend.users.models import Avatar

User = get_user_model()


class AvatarSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ["id", "photo", "name"]

    def get_name(self, obj):
        return Path(obj.photo.name).stem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserSearchSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "avatar"]


class UserDetailSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(read_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())], required=False
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "email",
            "avatar",
        ]
        read_only_fields = [
            "id",
            "avatar",
        ]


class BoardOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]


class BoardMemberSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "name", "avatar"]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

