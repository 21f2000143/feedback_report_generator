from django.db import models
from django.contrib.auth.models import AbstractUser


# Customizing the user model
class User(AbstractUser):
    USER_TYPES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=10, choices=USER_TYPES)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Report(models.Model):
    task_id = models.CharField(max_length=255)
    html_content = models.TextField(null=True, blank=True)
    pdf_content = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=20, default='PENDING')
    error = models.TextField(null=True, blank=True)
