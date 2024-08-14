from rest_framework import serializers
from .models import Complaints
from User.models import official

class ComplaintCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Complaints
        fields = ['complaint_id','User','complaint_details','complaint_location']

class ComplaintListSerializer(serializers.ModelSerializer):
    class Meta:
        model:Complaints
        fields = ['complaint_id','complaint_details','complaint_location','status','person_assigned','created_date']

class OfficialSerializer(serializers.ModelSerializer):
    class Meta:
        model = official
        fields = ['id','username']