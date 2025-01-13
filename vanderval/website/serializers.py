from rest_framework import serializers
from website.models import Site, UserRecords, Jobs

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Site
        fields = '__all__'
        
class UserRecordsSerializer(serializers.ModelSerializer):
     class Meta:
        model=UserRecords
        fields = '__all__'
class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Jobs
        fields="__all__"
    
        
    