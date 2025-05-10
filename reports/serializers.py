from rest_framework import serializers
from reports.models import (
    User,
    Report
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


class HtmlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ['task_id', 'html_content']


class CreateHtmlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ['task_id', 'html_content']


class PdfSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ['task_id', 'pdf_content']


class CreatePdfSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ['task_id', 'pdf_content']
