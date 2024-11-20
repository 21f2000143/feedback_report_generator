from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import generate_html_report, generate_pdf_report
from .models import Report
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import os
from .validation import validate_payload


class GenerateHTMLReportView(APIView):
    def post(self, request):
        # Validate the payload
        request_data = request.data
        if not validate_payload(request_data):
            return Response({'error': 'Invalid payload'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Start the task to generate the HTML report
        task = generate_html_report.delay(request_data)

        # Respond with the task ID
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class GetHTMLReportView(APIView):
    def get(self, request, task_id):
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


class GeneratePDFReportView(APIView):
    def post(self, request):
        # Validate the payload
        request_data = request.data
        if not validate_payload(request_data):
            return Response({'error': 'Invalid payload'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Start the task to generate the PDF report
        task = generate_pdf_report.delay(request_data)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class GetPDFReportView(APIView):
    def get(self, request, task_id):
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
