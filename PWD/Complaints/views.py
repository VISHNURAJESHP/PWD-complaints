from django.shortcuts import render
from .models import Compaints
from rest_framework.views import APIView
from .serializers import ComplaintCreationSerializer

class ComplaintCreation(APIView):
    def post(self,request):

        

        serializer = ComplaintCreationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(User=User)
