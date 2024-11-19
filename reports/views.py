from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import generate_html_report, generate_pdf_report
from .models import Report
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


class GenerateHTMLReportView(APIView):
    def post(self, request):
        task = generate_html_report.delay(request.data)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class GetHTMLReportView(APIView):
    def get(self, request, task_id):
        try:
            # Get the task result using the task_id
            task = generate_html_report.AsyncResult(task_id)
            if task.status == 'success':
                # Retrieve the report object if the task is successful
                report = get_object_or_404(Report, task_id=task_id)
                return HttpResponse(report.html_content,
                                    content_type='text/html')
            else:
                # Return task status if not successful yet
                return Response({'task_id': task_id, 'status': task.status,
                                 'info': task.info},
                                status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            # Handle exceptions and return error response
            return Response({'task_id': task_id, 'status': 'error',
                             'info': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class GeneratePDFReportView(APIView):
    def post(self, request):
        task = generate_pdf_report.delay(request.data)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class GetPDFReportView(APIView):
    def get(self, request, task_id):
        try:
            # Get the task result using the task_id
            task = generate_pdf_report.AsyncResult(task_id)
            if task.status == 'success':
                # Retrieve the report object if the task is successful
                report = get_object_or_404(Report, task_id=task_id)
                return HttpResponse(report.pdf_content,
                                    content_type='application/pdf')
            else:
                # Return task status if not successful yet
                return Response({'task_id': task_id, 'status': task.status,
                                 'info': task.info},
                                status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            # Handle exceptions and return error response
            return Response({'task_id': task_id, 'status': 'error',
                             'info': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
