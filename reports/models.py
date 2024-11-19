from django.db import models


class Report(models.Model):
    task_id = models.CharField(max_length=255)
    html_content = models.TextField(null=True, blank=True)
    pdf_content = models.URLField(null=True, blank=True)
