from typing import Iterable
from django.db import models
from django.contrib.auth.models import User

class JobPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.TextField()
    salary_range = models.TextField(max_length=50)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_post')

    def __str__(self):
        return f"{self.id} - {self.title}"