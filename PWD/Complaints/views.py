from django.shortcuts import render
from .models import Complaints
from rest_framework.views import APIView
from .serializers import ComplaintCreationSerializer
from .utils import authenticate_user
from rest_framework.response import Response
from rest_framework import status

class ComplaintCreation(APIView):
    def post(self, request):
        token = request.COOKIES.get("jwt")
        user = authenticate_user(token)
        try:
            serializer = ComplaintCreationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(User=user)
        except Exception as e:
            return Response({"error:""Provide all needed details"}, status = 400)

class ComplaintUpdation:
    def patch(self, request, complaint_id):
        token = request.COOKIES.get("jwt")
        user = authenticate_user(token)
        status = request.data.get('status')
        reason = request.data.get('reason')
        try:
            complaint = Complaints.objects.get(id=complaint_id)
        except Complaints.DoesNotExist:
            return Response({"error":"The complaint not found"},status=404)
        
        if user.is_staff:
            complaint.status = status
            complaint.reason = reason
            complaint.person_updated = user
            complaint.save()
            return Response({"message":"The complaint updated sucessfully"},status=200)
        else:
            return Response({"error":"You are not authorized update this complaint"},status=403)