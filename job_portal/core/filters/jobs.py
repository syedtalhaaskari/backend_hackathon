# filters.py
from django_filters import rest_framework as filters
from core.models.job_post import JobPost

class JobPostFilter(filters.FilterSet):
    city = filters.CharFilter(field_name="user__employer__city")
    country = filters.CharFilter(field_name="user__employer__country")
    skills = filters.CharFilter(field_name="skills", lookup_expr="icontains")
    company_name = filters.CharFilter(field_name="user__employer__company_name", lookup_expr="icontains")

    class Meta:
        model = JobPost
        fields = [
            "city",
            "country",
        ]