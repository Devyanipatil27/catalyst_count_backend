from django.db import models
from django.contrib.auth.models import AbstractUser


class CSVRecord(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    year_founded = models.IntegerField(null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    size_range = models.CharField(max_length=100, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    linkedin_url = models.URLField(max_length=500, null=True, blank=True)
    current_employee_estimate = models.IntegerField(null=True, blank=True)
    total_employee_estimate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class CompanyData(models.Model):
    name = models.CharField(max_length=255)
    # Upload directly to 'media/company_data/'
    csv_file = models.FileField(upload_to='')

    def __str__(self):
        return self.name
