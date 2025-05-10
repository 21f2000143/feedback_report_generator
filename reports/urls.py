from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.api_root),
    #     Below three paths are for user stuff
    path("user/", views.UserList.as_view(), name='user-list'),
    path("register-admin/", views.AdminRegisterAPIView.as_view()),
    path("register-student/", views.StudentRegisterAPIView.as_view()),
    #     Main api endpoints which are required for the assignment
    path('assignment/html', views.GenerateReportView.as_view(
      report_type='html'),
         name='generate-html-report'),
    path('assignment/html/<str:task_id>', views.GetReportView.as_view(
      report_type='html')),
    path('assignment/pdf', views.GenerateReportView.as_view(
      report_type='pdf'),
         name='generate-pdf-report'),
    path('assignment/pdf/<str:task_id>', views.GetReportView.as_view(
      report_type='pdf'
    )),
]

urlpatterns = format_suffix_patterns(urlpatterns)
