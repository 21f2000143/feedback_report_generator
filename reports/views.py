from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import generate_html_report, generate_pdf_report
from rest_framework import permissions
from uuid import uuid4
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from reports.permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import os
from .validation import validate_payload

from reports.models import (
    User,
    Report
)

from reports.serializers import (
    UserSerializer,
    AdminRegisterSerializer,
    StudentRegisterSerializer,
    InputSerializer
)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.filter(role='admin')
    serializer_class = AdminRegisterSerializer

    def perform_create(self, serializer):
        serializer.save()


class StudentRegisterAPIView(generics.CreateAPIView):
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

        task_id = str(uuid4())

        if self.report_type == 'html':
            generate_html_report.delay(validated)
        elif self.report_type == 'pdf':
            generate_pdf_report.delay(validated)

        return Response({"task_id": task_id}, status=status.HTTP_202_ACCEPTED)


class GetReportView(APIView):
    report_type = None
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, task_id, format=None):
        if self.report_type == 'html':
            try:
                # Get the task result using the task_id
                task = generate_html_report.AsyncResult(task_id)
                if task.status == 'SUCCESS':
                    # Retrieve the report object if the task is successful
                    report = get_object_or_404(Report, task_id=task_id)
                    return Response({
                        'task_id': task_id,
                        'status': task.status,
                        'html_content': report.html_content
                    }, status=status.HTTP_200_OK)
                elif task.status == 'FAILURE':
                    # Get the exception without propagating it
                    error_reason = task.get(propagate=False)
                    return Response({
                        'task_id': task_id,
                        'status': task.status,
                        'error': str(error_reason)
                    }, status=status.HTTP_202_ACCEPTED)
                else:
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
                # Get the task result using the task_id
                task = generate_pdf_report.AsyncResult(task_id)
                if task.status == 'SUCCESS':
                    # Retrieve the report object if the task is successful
                    report = get_object_or_404(Report, task_id=task_id)
                    file_path = report.pdf_content
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as fh:
                            response = HttpResponse(fh.read(),
                                                    content_type="application/pdf")
                            response['Content-Disposition'] = 'attachment; filename=' + \
                                os.path.basename(file_path)
                            return response

                    # If the file does not exist, return the status of the task
                    return Response({
                        'task_id': task_id,
                        'status': task.status
                    }, status=status.HTTP_202_ACCEPTED)
                elif task.status == 'FAILURE':
                    # Get the exception without propagating it
                    # Fetch the exception instance
                    error_reason = task.get(propagate=False)
                    return Response({
                        'task_id': task_id,
                        'status': task.status,
                        # Convert exception to string for JSON
                        'error': str(error_reason)
                    }, status=status.HTTP_202_ACCEPTED)
                else:
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
