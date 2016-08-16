from rest_framework import serializers

from .models import Company, Job


class CompanyAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'company_name', 'location', 'founded_year', 'opening', 'no_openings')


class JobAllSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(read_only=True, source="company.company_name")
    company_id = serializers.PrimaryKeyRelatedField(read_only=True)
    career_url = serializers.CharField(read_only=True, source="company.career_url")

    class Meta:
        model = Job
        fields = ('id', 'job_name', 'company_name', 'company_id', 'career_url')


class CompanySerializer(serializers.ModelSerializer):
    jobs = serializers.StringRelatedField(many=True)

    class Meta:
        model = Company
        fields = ('id', 'company_name', 'location', 'founded_year', 'opening', 'no_openings', 'company_url', 'career_url', 'jobs')




