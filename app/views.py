from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from rest_framework.response import Response

from app.serializers import ExcelFileSerializer

# Create your views here.
class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = ExcelFileSerializer(data=request.data)

        #Serializer checks if all the data is validated or not
        # If it is valid then the data is saved
        # If not then error is sent to the frontend
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



