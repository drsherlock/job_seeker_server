from rest_framework.response import Response
# from django.shortcuts import render, redirect
from .models import Company, Job
from .serializers import CompanyAllSerializer, JobAllSerializer, CompanySerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import re

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_companies(request):
    companies_list = Company.objects.all()
    paginator = PageNumberPagination()
    companies = paginator.paginate_queryset(companies_list, request)
    serializer = CompanyAllSerializer(companies, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_jobs(request):
    jobs_list = Job.objects.all()
    paginator = PageNumberPagination()
    jobs = paginator.paginate_queryset(jobs_list, request)
    serializer = JobAllSerializer(jobs, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_company(request, id):
    company = Company.objects.get(id=id)
    serializer = CompanySerializer(company)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((AllowAny,))
def search_companies(request, company):
    companies_list = Company.objects.filter(company_name__icontains=company)
    paginator = PageNumberPagination()
    companies = paginator.paginate_queryset(companies_list, request)
    serializer = CompanyAllSerializer(companies, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes((AllowAny,))
def search_jobs(request, job):
    jobs_list = Job.objects.filter(job_name__icontains=job)
    paginator = PageNumberPagination()
    jobs = paginator.paginate_queryset(jobs_list, request)
    serializer = JobAllSerializer(jobs, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def search_job(request, id, job_name):
    company = Company.objects.get(id=id)
    serializer = CompanySerializer(company)
    copy_list = list(serializer.data["jobs"])
    for i in range(len(copy_list)):
        if re.search(job_name, copy_list[i], re.IGNORECASE) is None:
            x = copy_list[i]
            serializer.data["jobs"].remove(x)
    return Response(serializer.data)