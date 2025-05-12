from rest_framework import serializers
from reports.models import (
    User,
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'role']


class AdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        validated_data['role'] = 'admin'
        user = User.objects.create_user(**validated_data)
        return user


class StudentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        validated_data['role'] = 'student'
        user = User.objects.create_user(**validated_data)
        return user


class EventSerializer(serializers.Serializer):
    type = serializers.CharField()
    created_time = serializers.DateTimeField()
    unit = serializers.CharField()


class InputSerializer(serializers.Serializer):
    namespace = serializers.CharField()
    student_id = serializers.CharField()
    events = EventSerializer(many=True)
