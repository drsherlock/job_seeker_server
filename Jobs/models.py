from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    founded_year = models.CharField(max_length=5)
    company_url = models.CharField(max_length=1000)
    career_url = models.CharField(max_length=1000)
    opening = models.BooleanField(default=False)
    no_openings = models.IntegerField(default=0)

    def __unicode__(self):
        return self.company_name


class Job(models.Model):
    company = models.ForeignKey(Company, related_name='jobs')
    job_name = models.CharField(max_length=250)

    def __unicode__(self):
        return self.job_name
