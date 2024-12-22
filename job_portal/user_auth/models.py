from django.contrib.auth.models import User
from django.db import models

class JobSeeker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobseeker')
    gender = models.CharField(max_length=6, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.FileField(upload_to=f'profile_image/', blank=True, null=True)
    cv_file = models.FileField(upload_to=f'cv/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.user.username

class Employer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employer')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to=f'profile_image/', blank=True, null=True)
    company_size= models.CharField(max_length=255, blank=True, null=True)
    
    is_verified = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.user.username