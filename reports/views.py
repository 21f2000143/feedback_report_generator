from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import generate_html_report, generate_pdf_report
from rest_framework import permissions
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from reports.permissions import IsOwnerOrReadOnly
from django.http import HttpResponse
import os
from config.celery import app

from reports.models import (
    User,
    Report
)

from reports.serializers import (
    UserSerializer,
    AdminRegisterSerializer,
    StudentRegisterSerializer,
    InputSerializer,
)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'register-admin': reverse('admin-register', request=request,
                                  format=format),
        'register-student': reverse('student-register', request=request,
                                    format=format),
        'generate-html-report': reverse('generate-html-report',
                                        request=request, format=format),
        'generate-pdf-report': reverse('generate-pdf-report',
                                       request=request, format=format),
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminRegisterAPIView(generics.ListCreateAPIView):
    queryset = User.objects.filter(role='admin')
    serializer_class = AdminRegisterSerializer

    def perform_create(self, serializer):
        serializer.save()


class StudentRegisterAPIView(generics.ListCreateAPIView):
    queryset = User.objects.filter(role='student')
    serializer_class = StudentRegisterSerializer

    def perform_create(self, serializer):
        serializer.save()


class GenerateReportView(generics.CreateAPIView):
    report_type = None
    serializer_class = InputSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        if self.report_type == 'html':
            task = generate_html_report.delay(validated)
        elif self.report_type == 'pdf':
            task = generate_pdf_report.delay(validated)

        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)


class GetReportView(APIView):
    report_type = None
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, task_id, format=None):
        report = Report.objects.filter(task_id=task_id).first()
        if self.report_type == 'html':
            try:
                if report:
                    # If the report exists, return the HTML content
                    if report.status == 'SUCCESS':
                        return Response({
                            'task_id': task_id,
                            'status': report.status,
                            'html_content': report.html_content
                        }, status=status.HTTP_200_OK)
                    elif report.status == 'FAILURE':
                        # If the report failed, return the error message
                        return Response({
                            'task_id': task_id,
                            'status': report.status,
                            'error': report.error
                        }, status=status.HTTP_202_ACCEPTED)
                else:
                    # Get the task result using the task_id
                    task = generate_html_report.AsyncResult(task_id)
                    # For states like PENDING or STARTED
                    return Response({
                        'task_id': task_id,
                        'status': task.status
                    }, status=status.HTTP_202_ACCEPTED)
            except Exception as e:
                # Handle exceptions and return error response
                return Response({'task_id': task_id, 'status': 'error',
                                 'info': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
        elif self.report_type == 'pdf':
            try:
                # Check if the report exists
                if report:
                    # If the report exists, return the PDF content
                    if report.status == 'SUCCESS':
                        file_path = report.pdf_content
                        if os.path.exists(file_path):
                            with open(file_path, 'rb') as fh:
                                response = HttpResponse(
                                    fh.read(), content_type="application/pdf")
                                response['Content-Disposition'] = 'attachment;\
                                    filename=' + os.path.basename(file_path)
                                return response
                        else:
                            return Response({
                                'task_id': task_id,
                                'status': report.status,
                                'error': 'File not found'
                            }, status=status.HTTP_404_NOT_FOUND)
                    elif report.status == 'FAILURE':
                        # If the report failed, return the error message
                        return Response({
                            'task_id': task_id,
                            'status': report.status,
                            'error': report.error
                        }, status=status.HTTP_202_ACCEPTED)
                else:
                    # Get the task result using the task_id
                    task = generate_pdf_report.AsyncResult(task_id, app=app)
                    # For states like PENDING or STARTED
                    return Response({
                        'task_id': task_id,
                        'status': task.status
                    }, status=status.HTTP_202_ACCEPTED)
            except Exception as e:
                # Handle exceptions and return error response
                return Response({'task_id': task_id, 'status': 'error',
                                'info': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
