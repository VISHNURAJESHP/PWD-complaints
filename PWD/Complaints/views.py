from django.shortcuts import render
from .models import Complaints
from User.models import official
from rest_framework.views import APIView
from .serializers import ComplaintCreationSerializer,ComplaintListSerializer,OfficialSerializer
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
            complaint.save()
            return Response({"message":"The complaint updated sucessfully"},status=200)
        else:
            return Response({"error":"You are not authorized update this complaint"},status=403)
        
class OfficialComplaints(APIView):

    #Return the list of complaints of the wing
    def get(self,request):
        token = request.COOKIES.get('jwt')
        user = authenticate_user(token)
        wing=user.wing
        try:
            complaint_list=Complaints.objects.filter(wing=wing)
        except:
            return Response({"error":"There is no complaints"},status=403)
        
        try:
            officals_list = official.objects.filter(wing=wing, head_of_wing=False)
        except:
            return Response({"error":"There is no official"},status=403)
        
        complaint_serializer = ComplaintListSerializer(complaint_list, many=True)
        official_serializer = OfficialSerializer(officals_list, many=True)

        return Response({"complaints":complaint_serializer.data, "officials":official_serializer.data})
    
    #assign a complaint to a person
    def post(self,request,complaint_id):
        token = request.COOKIES.get('jwt')
        user = authenticate_user(token)
        person_id = request.data.get('person')
        try:
            complaint = Complaints.objects.get(id=complaint_id)
        except Complaints.DoesNotExist:
            return Response({"error":"The complaint not found"},status=404)
        
        try:
            assigned_person = official.objects.get(id=person_id)
        except:
            return Response({"error":"The person not found"},status=403)
        
        if user.head_of_wing:
            complaint.person_assigned = assigned_person
            complaint.save()
            return Response({"message":"The person assigned sucessfully"},status=200)
        else:
            return Response({"error":"You are not authorized assign an person"},status=403)

