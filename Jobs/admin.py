from django.contrib import admin

# Register your models here.

from .models import Company, Job


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'location', 'founded_year', 'opening']
    list_filter = ['location', 'founded_year', 'opening']
    search_fields = ['company_name']


class JobAdmin(admin.ModelAdmin):
    list_display = ['job_name', 'company']
    readonly_fields = ['company']
    search_fields = ['job_name']


admin.site.register(Company, CompanyAdmin)
admin.site.register(Job, JobAdmin)
