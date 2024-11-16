from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .job_post import JobPost

class Application(models.Model):
    class STATUS(models.TextChoices):
        Applied = 'Applied', _('Applied')
        Approved = 'Approved', _('Approved')
        Rejected = 'Rejected', _('Rejected')
        Hired = 'Hired', _('Hired')

    status = models.CharField(
        max_length=10,
        choices=STATUS.choices,
        default=STATUS.Applied,
    )
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='application')
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='application')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}"