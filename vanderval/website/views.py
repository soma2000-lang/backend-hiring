from website.models import Site, UserRecords, Jobs
from website.serializers import SiteSerializer, UserRecordsSerializer, JobsSerializer 
from website.tasks import distributer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.pagination import PageNumberPagination
import logging

logger = logging.getLogger(__name__)
from django.http import HttpResponse


class SiteListAPIView(APIView):
    
    def get(self, request):
        sites = Site.objects.all().order_by('-pk')
        paginator = PageNumberPagination()
        paginator.page_size = 5
        paginated_sites = paginator.paginate_queryset(sites, request)
        serializer = SiteSerializer(paginated_sites, many=True)
        return paginator.get_paginated_response(serializer.data) 
    def post(self,request):
        with transaction.atomic():
            serializer=SiteSerializer(data=request.data)
            if(serializer.is_valid()):
                serializer.save()
                return Response(data=serializer.data)
            else: return HttpResponse(serializer.errors)
class UsersRecordListAPIView(APIView):
    
    def get(self, request):
        users = UserRecords.objects.all().order_by('-pk')
        paginator = PageNumberPagination()
        paginator.page_size = 5
        paginated_sites = paginator.paginate_queryset(users, request)
        serializer = UserRecordsSerializer(paginated_sites,many=True)
        return paginator.get_paginated_response(serializer.data)  
    def post(self,request):
        with transaction.atomic():
            serializer=UserRecordsSerializer(data=request.data)
            if(serializer.is_valid()): 
                serializer.save()
                return Response(data=serializer.data)
            else: return HttpResponse(serializer.errors)
class JobListAPIView(APIView):
    
    def get(self, request):
        jobs = Jobs.objects.all().order_by('-pk')
        paginator = PageNumberPagination()
        paginator.page_size = 5
        paginated_sites = paginator.paginate_queryset(jobs, request)
        serializer = JobsSerializer(paginated_sites,many=True)
        return paginator.get_paginated_response(serializer.data) 
    def post(self,request):
        with transaction.atomic():
            serializer=JobsSerializer(data=request.data)
  
            if(serializer.is_valid()):  
                distributer.delay()
                serializer.save()
                return Response(data=serializer.data)
            else: return HttpResponse(serializer.errors)
            
            