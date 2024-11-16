from django.urls import path
from . import views

urlpatterns = [
    path('html', views.GenerateHTMLReportView.as_view(), name='generate-html-report'),
    path('html/<str:task_id>', views.GetHTMLReportView.as_view(), name='get-html-report'),
    path('pdf', views.GeneratePDFReportView.as_view(), name='generate-pdf-report'),
    path('pdf/<str:task_id>', views.GetPDFReportView.as_view(), name='get-pdf-report'),
]
