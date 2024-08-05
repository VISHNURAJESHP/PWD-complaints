from rest_framework import serializers
from .models import Compaints

class ComplaintCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Compaints
        fields =['complaint_id','User','complaint_details','complaint_location']