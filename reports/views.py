from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import generate_html_report, generate_pdf_report
from .models import Report
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


class GenerateHTMLReportView(APIView):
    def post(self, request):
        print(request.data)
        task = generate_html_report.delay(request.data)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class GetHTMLReportView(APIView):
    def get(self, request, task_id):
        report = get_object_or_404(Report, task_id=task_id)
        return Response({'html': report.html_content})


class GeneratePDFReportView(APIView):
    def post(self, request):
        task = generate_pdf_report.delay(request.data)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class GetPDFReportView(APIView):
    def get(self, request, task_id):
        report = get_object_or_404(Report, task_id=task_id)
        response = HttpResponse(
            report.pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; \
            filename="report_{task_id}.pdf"'
        return response
