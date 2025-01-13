from django.urls import path
from website.views import (
   SiteListAPIView,
   UsersRecordListAPIView, 
   JobListAPIView
)

app_name = 'website'

urlpatterns = [

   path('sites/', SiteListAPIView.as_view(), name='site-list'),
   path('users/', UsersRecordListAPIView.as_view(), name='user-record-list'),
   path('jobs/', JobListAPIView.as_view(), name='job-list'),
]